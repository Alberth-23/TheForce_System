from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
from app.core.db import Base
import enum
from datetime import datetime

class TipoTrabajo(str, enum.Enum):
    Mantenimiento_preventivo = "Mantenimiento preventivo"
    Inspeccion = "Inspeccion"
    Reparacion = "Reparacion"

class TipoAceite(str, enum.Enum):
    Lubripowe_20W_50 = "Lubripowe 20W-50"
    SEMI_SINTETICO_10W_30 = "SEMI-SINTETICO 10W-30"
    SINTETICO_10W_30 = "SINTETICO 10W-30"

class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, index=True)
    nombre_empresa = Column(String, nullable=False)
    clientes = relationship("Cliente", back_populates="empresa")

class Cliente(Base):
    __tablename__ = "clientes"
    id_cliente = Column(Integer, primary_key=True, index=True)
    dni = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    celular = Column(String)
    cip = Column(String)
    id_empresa = Column(Integer, ForeignKey("empresas.id"))
    
    empresa = relationship("Empresa", back_populates="clientes")
    ordenes = relationship("OrdenServicio", back_populates="cliente")

class Vehiculo(Base):
    __tablename__ = "vehiculos"
    placa = Column(String, primary_key=True, index=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    color = Column(String)
    kilometraje_ingreso = Column(Integer, nullable=False)
    ordenes = relationship("OrdenServicio", back_populates="vehiculo")

class OrdenServicio(Base):
    __tablename__ = "ordenes_servicio"
    id_orden = Column(Integer, primary_key=True, index=True)
    numero_orden = Column(String, unique=True, index=True, nullable=False)
    fecha_ingreso = Column(DateTime, default=datetime.now)
    fecha_salida = Column(DateTime)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    placa_vehiculo = Column(String, ForeignKey("vehiculos.placa"), nullable=False)
    kilometraje_actual = Column(Integer, nullable=False)
    tipo_aceite = Column(String, nullable=False) # Simplified for compatibility with existing enums
    tipo_trabajo = Column(String, nullable=False)
    requirimientos_cliente = Column(Text)
    trabajos_realizados = Column(Text)
    repuestos_cambiados = Column(Text)
    entregada = Column(Boolean, default=False)
    nombre_recoge = Column(String)
    proximo_mantenimiento_km = Column(Integer)
    costo_mano_obra = Column(Float, default=0.0)
    costo_repuestos = Column(Float, default=0.0)
    total_pagar = Column(Float, default=0.0)
    metodo_pago = Column(String)


    cliente = relationship("Cliente", back_populates="ordenes")

    vehiculo = relationship("Vehiculo", back_populates="ordenes")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="admin") # admin, mechanic

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    modelo = Column(String)
    aplicacion = Column(String) # Para qué unidad
    marca_tipo = Column(String) # Honda / Alternativo
    es_novaflat = Column(Boolean, default=False)
    stock = Column(Integer, default=0)
    precio_compra = Column(Float, default=0.0)
    precio_venta = Column(Float, default=0.0)
    ingresos_totales = Column(Integer, default=0)
    salidas_totales = Column(Integer, default=0)
class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    tipo = Column(String) # entrada / salida
    cantidad = Column(Integer)
    fecha = Column(DateTime, default=datetime.now)
    placa_vehiculo = Column(String) # Opcional para salidas
    numero_orden = Column(String)   # Opcional para salidas
    
    producto = relationship("Producto")
class OrdenRepuesto(Base):
    __tablename__ = "orden_repuestos"
    id = Column(Integer, primary_key=True, index=True)
    id_orden = Column(Integer, ForeignKey("ordenes_servicio.id_orden"))
    id_producto = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, default=1)
    precio_unitario = Column(Float)
    
    orden = relationship("OrdenServicio", back_populates="repuestos_lista")
    producto = relationship("Producto")

# Update OrdenServicio relationship
OrdenServicio.repuestos_lista = relationship("OrdenRepuesto", back_populates="orden")
