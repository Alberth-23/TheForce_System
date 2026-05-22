from fastapi import APIRouter, Depends, Request, Form, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.domain import Cliente, Vehiculo, OrdenServicio, Empresa, Producto, MovimientoInventario, OrdenRepuesto
from datetime import datetime

from app.services.pdf_service import render_to_pdf

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

from app.services.api_service import buscar_dni

@router.get("/api/buscar_dni/{dni}")
async def api_buscar_dni(dni: str):
    return buscar_dni(dni)

import json

@router.get("/ordenes/{num_orden}/pdf")
async def descargar_pdf(num_orden: str, db: Session = Depends(get_db)):
    orden = db.query(OrdenServicio).filter(OrdenServicio.numero_orden == num_orden).first()
    if not orden:
        return {"error": "Orden no encontrada"}
    
    # Intentar parsear JSON de trabajos y repuestos
    try:
        trabajos_list = json.loads(orden.trabajos_realizados) if orden.trabajos_realizados else []
    except:
        trabajos_list = [{"desc": orden.trabajos_realizados, "price": orden.costo_mano_obra}] if orden.trabajos_realizados else []

    try:
        repuestos_list = json.loads(orden.repuestos_cambiados) if orden.repuestos_cambiados else []
    except:
        repuestos_list = [{"desc": orden.repuestos_cambiados, "price": orden.costo_repuestos}] if orden.repuestos_cambiados else []

    subtotal = orden.total_pagar / 1.18
    igv = orden.total_pagar - subtotal

    pdf_content = render_to_pdf("pdf_orden.html", {
        "orden": orden, 
        "trabajos": trabajos_list,
        "repuestos": repuestos_list,
        "subtotal": subtotal,
        "igv": igv,
        "datetime": datetime
    })


    if pdf_content:
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=Orden_{num_orden}.pdf"}
        )
    return {"error": "Error al generar PDF"}

@router.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    stats = {
        "total_ordenes": db.query(OrdenServicio).count(),
        "pendientes": db.query(OrdenServicio).filter(OrdenServicio.entregada == False).count(),
        "hoy": db.query(OrdenServicio).filter(OrdenServicio.fecha_ingreso >= datetime.now().date()).count(),
        "alertas_stock": db.query(Producto).filter(Producto.stock < 5).all()
    }

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html", 
        context={"active_page": "dashboard", "stats": stats}
    )


@router.get("/nueva_orden")
async def view_nueva_orden(request: Request, success_msg: str = None):
    return templates.TemplateResponse(
        request=request,
        name="index.html", 
        context={"active_page": "nueva_orden", "success_msg": success_msg}
    )


@router.post("/registrar_orden")
async def registrar_orden(
    request: Request,
    dni: str = Form(...),
    nombre: str = Form(...),
    apellido: str = Form(...),
    celular: str = Form(None),
    cip: str = Form(None),
    placa: str = Form(...),
    marca: str = Form(...),
    modelo: str = Form(...),
    color: str = Form(None),
    km_actual: int = Form(...),
    tipo_trabajo: str = Form(...),
    tipo_aceite: str = Form(...),
    requerimientos: str = Form(None),
    es_novaflat: bool = Form(False),

    db: Session = Depends(get_db)
):
    # 1. Manejar Empresa (Novaflat)
    empresa_id = None
    if es_novaflat:
        empresa = db.query(Empresa).filter(Empresa.nombre_empresa == "Novaflat").first()
        if not empresa:
            empresa = Empresa(nombre_empresa="Novaflat")
            db.add(empresa)
            db.flush()
        empresa_id = empresa.id

    # 2. Manejar Cliente
    cliente = db.query(Cliente).filter(Cliente.dni == dni).first()
    if cliente:
        cliente.nombre = nombre
        cliente.apellido = apellido
        cliente.celular = celular
        cliente.cip = cip
        if empresa_id:
            cliente.id_empresa = empresa_id
    else:
        cliente = Cliente(dni=dni, nombre=nombre, apellido=apellido, celular=celular, cip=cip, id_empresa=empresa_id)
        db.add(cliente)
    db.flush() # Para obtener el id_cliente


    # 2. Manejar Vehículo
    vehiculo = db.query(Vehiculo).filter(Vehiculo.placa == placa).first()
    if vehiculo:
        vehiculo.marca = marca
        vehiculo.modelo = modelo
        if color:
            vehiculo.color = color
    else:
        vehiculo = Vehiculo(placa=placa, marca=marca, modelo=modelo, color=color, kilometraje_ingreso=km_actual)
        db.add(vehiculo)
    
    # 3. Orden
    num_orden = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    nueva_orden = OrdenServicio(
        numero_orden=num_orden,
        id_cliente=cliente.id_cliente,
        placa_vehiculo=placa,
        kilometraje_actual=km_actual,
        tipo_aceite=tipo_aceite,
        tipo_trabajo=tipo_trabajo,
        requirimientos_cliente=requerimientos
    )
    db.add(nueva_orden)
    db.commit()

    from urllib.parse import quote
    return RedirectResponse(
        url=f"/nueva_orden?success_msg={quote(f'Orden {num_orden} registrada con éxito')}",
        status_code=303
    )


@router.get("/ordenes")
async def listar_ordenes(request: Request, db: Session = Depends(get_db)):
    ordenes = db.query(OrdenServicio).join(Cliente).order_by(OrdenServicio.fecha_ingreso.desc()).all()
    # Mapear resultados a diccionarios para compatibilidad con el template actual o actualizar el template
    return templates.TemplateResponse(
        request=request,
        name="listado.html",
        context={"active_page": "ordenes", "ordenes": ordenes}
    )


@router.get("/clientes")
async def listar_clientes(request: Request, db: Session = Depends(get_db)):
    clientes = db.query(Cliente).order_by(Cliente.apellido.asc()).all()
    return templates.TemplateResponse(
        request=request,
        name="clientes.html",
        context={"active_page": "clientes", "clientes": clientes}
    )


@router.get("/vehiculos")
async def listar_vehiculos(request: Request, db: Session = Depends(get_db)):
    vehiculos = db.query(Vehiculo).order_by(Vehiculo.placa.asc()).all()
    return templates.TemplateResponse(
        request=request,
        name="vehiculos.html",
        context={"active_page": "vehiculos", "vehiculos": vehiculos}
    )


@router.post("/entregar_orden/{num_orden}")
async def entregar_orden(num_orden: str, nombre_recoge: str = Form(None), db: Session = Depends(get_db)):
    orden = db.query(OrdenServicio).filter(OrdenServicio.numero_orden == num_orden).first()
    if orden:
        orden.entregada = True
        orden.fecha_salida = datetime.now()
        orden.nombre_recoge = nombre_recoge
        db.commit()
        return {"status": "success"}
    return {"status": "error"}

@router.post("/revertir_entrega/{num_orden}")
async def revertir_entrega(num_orden: str, db: Session = Depends(get_db)):
    orden = db.query(OrdenServicio).filter(OrdenServicio.numero_orden == num_orden).first()
    if orden:
        orden.entregada = False
        orden.fecha_salida = None
        orden.nombre_recoge = None
        db.commit()
        return {"status": "success"}
    return {"status": "error"}

@router.get("/ordenes/{num_orden}")
async def ver_detalle_orden(request: Request, num_orden: str, db: Session = Depends(get_db)):
    orden = db.query(OrdenServicio).filter(OrdenServicio.numero_orden == num_orden).first()
    if not orden:
        return {"error": "Orden no encontrada"}
    
    productos = db.query(Producto).filter(Producto.stock > 0).all()
    
    return templates.TemplateResponse(
        request=request,
        name="detalle_orden.html",
        context={"active_page": "ordenes", "orden": orden, "productos": productos}
    )

@router.post("/ordenes/{num_orden}/actualizar")
async def actualizar_orden(
    num_orden: str,
    trabajos: str = Form(None),
    repuestos: str = Form(None),
    costo_mano_obra: float = Form(0.0),
    costo_repuestos: float = Form(0.0),
    total_pagar: float = Form(0.0),
    metodo_pago: str = Form(None),
    proximo_mantenimiento_km: str = Form(None),
    db: Session = Depends(get_db)
):
    orden = db.query(OrdenServicio).filter(OrdenServicio.numero_orden == num_orden).first()
    if orden:
        orden.trabajos_realizados = trabajos
        orden.repuestos_cambiados = repuestos
        orden.costo_mano_obra = costo_mano_obra
        orden.costo_repuestos = costo_repuestos
        orden.total_pagar = total_pagar
        orden.metodo_pago = metodo_pago
        
        prox_km = None
        if proximo_mantenimiento_km and proximo_mantenimiento_km.strip() != "":
            try:
                prox_km = int(proximo_mantenimiento_km)
            except ValueError:
                pass
        orden.proximo_mantenimiento_km = prox_km
        
        db.commit()

        return {"status": "success"}
    return {"status": "error"}


@router.get("/empresas")
async def listar_empresas(request: Request, db: Session = Depends(get_db)):
    empresas = db.query(Empresa).all()
    return templates.TemplateResponse(
        request=request,
        name="empresas.html",
        context={"active_page": "empresas", "empresas": empresas}
    )

@router.get("/empresas/{id_empresa}")
async def detalle_empresa(request: Request, id_empresa: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == id_empresa).first()
    if not empresa:
        return {"error": "Empresa no encontrada"}
    
    # Obtener todas las órdenes vinculadas a clientes de esta empresa
    ordenes = db.query(OrdenServicio).join(Cliente).filter(Cliente.id_empresa == id_empresa).order_by(OrdenServicio.fecha_ingreso.desc()).all()
    
    return templates.TemplateResponse(
        request=request,
        name="detalle_empresa.html",
        context={"active_page": "empresas", "empresa": empresa, "ordenes": ordenes}
    )
@router.get("/inventario")
async def view_inventario(request: Request, db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    # Historial de últimos 20 movimientos
    historial = db.query(MovimientoInventario).order_by(MovimientoInventario.fecha.desc()).limit(20).all()
    return templates.TemplateResponse(
        request=request,
        name="inventario.html",
        context={
            "active_page": "inventario", 
            "productos": productos, 
            "historial": historial,
            "now_date": datetime.now().strftime('%Y-%m-%d')
        }
    )
@router.get("/inventario/movimientos")
async def view_movimientos(request: Request, db: Session = Depends(get_db)):
    movimientos = db.query(MovimientoInventario).order_by(MovimientoInventario.fecha.desc()).all()
    return templates.TemplateResponse(
        request=request,
        name="movimientos.html",
        context={"active_page": "inventario", "movimientos": movimientos}
    )

@router.post("/inventario/registrar")
async def registrar_producto(
    nombre: str = Form(...),
    modelo: str = Form(None),
    aplicacion: str = Form(None),
    marca_tipo: str = Form(...),
    es_novaflat: bool = Form(False),
    precio_compra: float = Form(0.0),
    precio_venta: float = Form(0.0),
    db: Session = Depends(get_db)
):
    print(f"DEBUG: Registrando producto {nombre}")
    nuevo = Producto(

        nombre=nombre, modelo=modelo, aplicacion=aplicacion,
        marca_tipo=marca_tipo, es_novaflat=es_novaflat,
        precio_compra=precio_compra, precio_venta=precio_venta,
        stock=0
    )
    db.add(nuevo)
    db.commit()
    return RedirectResponse(url="/inventario", status_code=303)

@router.post("/inventario/movimiento")
async def registrar_movimiento(
    producto_id: int = Form(...),
    tipo: str = Form(...), # 'entrada' o 'salida'
    cantidad: int = Form(...),
    placa_vehiculo: str = Form(None),
    numero_orden: str = Form(None),
    fecha_mov: str = Form(None),
    db: Session = Depends(get_db)
):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if producto:
        # Parsear fecha si viene
        fecha = datetime.now()
        if fecha_mov:
            try:
                fecha = datetime.strptime(fecha_mov, '%Y-%m-%d')
            except:
                pass

        if tipo == 'entrada':
            producto.stock += cantidad
            producto.ingresos_totales += cantidad
        elif tipo == 'salida':
            if producto.stock >= cantidad:
                producto.stock -= cantidad
                producto.salidas_totales += cantidad
            else:
                return RedirectResponse(url="/inventario?error=stock_insuficiente", status_code=303)
        
        # Registrar el movimiento
        mov = MovimientoInventario(
            producto_id=producto_id,
            tipo=tipo,
            cantidad=cantidad,
            placa_vehiculo=placa_vehiculo,
            numero_orden=numero_orden,
            fecha=fecha
        )

        db.add(mov)
        db.commit()
    return RedirectResponse(url="/inventario", status_code=303)

@router.post("/ordenes/{num_orden}/agregar_repuesto")
async def agregar_repuesto_orden(
    num_orden: str,
    producto_id: int = Form(...),
    cantidad: int = Form(...),
    db: Session = Depends(get_db)
):
    orden = db.query(OrdenServicio).filter(OrdenServicio.numero_orden == num_orden).first()
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    
    if orden and producto and producto.stock >= cantidad:
        # 1. Restar stock
        producto.stock -= cantidad
        producto.salidas_totales += cantidad
        
        # 2. Registrar movimiento inventario
        mov = MovimientoInventario(
            producto_id=producto_id,
            tipo='salida',
            cantidad=cantidad,
            placa_vehiculo=orden.placa_vehiculo,
            numero_orden=num_orden,
            fecha=datetime.now()
        )
        db.add(mov)
        
        # 3. Vincular a la orden
        item = OrdenRepuesto(
            id_orden=orden.id_orden,
            id_producto=producto_id,
            cantidad=cantidad,
            precio_unitario=producto.precio_venta
        )
        db.add(item)
        
        # 4. Actualizar costos de la orden
        orden.costo_repuestos += (producto.precio_venta * cantidad)
        orden.total_pagar = orden.costo_mano_obra + orden.costo_repuestos
        
        db.commit()
        
    return RedirectResponse(url=f"/ordenes/{num_orden}", status_code=303)

@router.post("/ordenes/{num_orden}/eliminar_repuesto/{item_id}")
async def eliminar_repuesto_orden(
    num_orden: str,
    item_id: int,
    db: Session = Depends(get_db)
):
    item = db.query(OrdenRepuesto).filter(OrdenRepuesto.id == item_id).first()
    orden = db.query(OrdenServicio).filter(OrdenServicio.numero_orden == num_orden).first()
    
    if item and orden:
        producto = db.query(Producto).filter(Producto.id == item.id_producto).first()
        if producto:
            # Revertir stock
            producto.stock += item.cantidad
            producto.salidas_totales -= item.cantidad
            
            # Revertir costos
            orden.costo_repuestos -= (item.precio_unitario * item.cantidad)
            orden.total_pagar = orden.costo_mano_obra + orden.costo_repuestos
            
            db.delete(item)
            db.commit()
            
    return RedirectResponse(url=f"/ordenes/{num_orden}", status_code=303)

