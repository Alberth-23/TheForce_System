import requests
import sys

BASE_URL = "http://localhost:8000"

def get_product_id_from_db():
    try:
        from app.core.db import SessionLocal
        from app.models.domain import Producto
        db = SessionLocal()
        p = db.query(Producto).first()
        prod_id = p.id if p else None
        db.close()
        return prod_id
    except Exception as e:
        print(f"Error fetching product ID from DB: {e}")
        return None

def test_flow():
    session = requests.Session()
    
    # 1. Login
    print("Testing /login...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    r = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
    print(f"Login Response: {r.status_code}")
    print(f"Cookies: {session.cookies.get_dict()}")
    assert r.status_code in [200, 303, 302], f"Login failed: {r.status_code}"

    # 2. Test /logout redirect code
    print("\nTesting /logout redirect...")
    r_logout = session.get(f"{BASE_URL}/logout", allow_redirects=False)
    print(f"Logout status: {r_logout.status_code}")
    print(f"Logout headers Location: {r_logout.headers.get('Location')}")
    assert r_logout.status_code == 303, f"Logout did not redirect with 303: {r_logout.status_code}"
    assert r_logout.headers.get('Location') == "/login"

    # Re-login to get access token for subsequent tests
    session.post(f"{BASE_URL}/login", data=login_data)

    # 3. Test /registrar_orden PRG redirection
    print("\nTesting /registrar_orden PRG redirect...")
    order_data = {
        "dni": "12345678",
        "nombre": "Maria Elena",
        "apellido": "Garcia Ruiz",
        "celular": "987654321",
        "es_novaflat": "false",
        "cip": "",
        "placa": "ABC-999",
        "marca": "Yamaha",
        "modelo": "R15",
        "color": "Azul",
        "km_actual": "5000",
        "tipo_trabajo": "Inspeccion",
        "tipo_aceite": "Lubripower 20W-50",
        "requerimientos": "Cambio de bujia"
    }
    r_order = session.post(f"{BASE_URL}/registrar_orden", data=order_data, allow_redirects=False)
    print(f"Register Order status: {r_order.status_code}")
    print(f"Register Order headers Location: {r_order.headers.get('Location')}")
    assert r_order.status_code == 303, f"Register Order did not redirect with 303: {r_order.status_code}"
    assert "success_msg=" in r_order.headers.get('Location')

    # Get the order number from the redirect URL
    import urllib.parse
    loc = r_order.headers.get('Location')
    parsed_loc = urllib.parse.urlparse(loc)
    query_params = urllib.parse.parse_qs(parsed_loc.query)
    success_msg = query_params.get('success_msg', [''])[0]
    print(f"Success message: {success_msg}")
    
    # Extract order number e.g. "Orden ORD-2026... registrada con éxito"
    # Word at index 1 is the order number
    parts = success_msg.split(" ")
    order_num = parts[1] if len(parts) > 1 else None
    print(f"Extracted Order Number: {order_num}")

    if order_num:
        # 4. Test /ordenes/{num_orden}/actualizar with empty proximo_mantenimiento_km
        print(f"\nTesting /ordenes/{order_num}/actualizar with empty maintenance km...")
        update_data = {
            "trabajos": '[]',
            "repuestos": '[]',
            "costo_mano_obra": 0.0,
            "costo_repuestos": 0.0,
            "total_pagar": 0.0,
            "metodo_pago": "Efectivo",
            "proximo_mantenimiento_km": "" # Sending empty string
        }
        r_update = session.post(f"{BASE_URL}/ordenes/{order_num}/actualizar", data=update_data)
        print(f"Update Order status: {r_update.status_code}")
        print(f"Update Order response: {r_update.text}")
        assert r_update.status_code == 200, f"Update failed with status: {r_update.status_code}"
        assert r_update.json().get('status') == "success"

    # Create a product via API to make sure we have at least one product
    print("\nCreating a test product via /inventario/registrar...")
    prod_data = {
        "nombre": "Filtro de Aceite Honda",
        "modelo": "CB190R",
        "aplicacion": "Honda",
        "marca_tipo": "Original",
        "es_novaflat": "false",
        "stock": "10",
        "precio_compra": "15.0",
        "precio_venta": "25.0"
    }
    r_prod = session.post(f"{BASE_URL}/inventario/registrar", data=prod_data, allow_redirects=False)
    print(f"Create Product status: {r_prod.status_code}")
    assert r_prod.status_code == 303, f"Product creation did not redirect: {r_prod.status_code}"

    # Get the product ID from DB
    prod_id = get_product_id_from_db()
    print(f"Product ID from database: {prod_id}")
    assert prod_id is not None, "Failed to retrieve product ID from database"

    # 5. Test /inventario/movimiento with insufficient stock redirect
    print("\nTesting /inventario/movimiento stock insufficient redirect...")
    mov_data = {
        "producto_id": prod_id,
        "tipo": "salida",
        "cantidad": 99999, # Large quantity to trigger stock insufficient
        "placa_vehiculo": "ABC-999",
        "numero_orden": order_num or "ORD-12345",
        "fecha_mov": ""
    }
    r_mov = session.post(f"{BASE_URL}/inventario/movimiento", data=mov_data, allow_redirects=False)
    print(f"Movement Register status: {r_mov.status_code}")
    print(f"Movement Register Location: {r_mov.headers.get('Location')}")
    assert r_mov.status_code == 303, f"Movement did not redirect with 303: {r_mov.status_code}"
    assert r_mov.headers.get('Location') == "/inventario?error=stock_insuficiente"

    print("\nAll integration API tests passed successfully!")

if __name__ == "__main__":
    test_flow()
