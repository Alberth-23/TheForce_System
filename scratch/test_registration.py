import psycopg2
from database import get_db_connection
from datetime import datetime

def test_registration():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect")
        return

    try:
        cur = conn.cursor()
        
        # Test Data
        dni = "77777777"
        nombre = "Test"
        apellido = "User"
        placa = "TST-999"
        marca = "TestBrand"
        modelo = "TestModel"
        km_actual = 1500
        tipo_trabajo = "Inspeccion"
        tipo_aceite = "Lubripowe 20W-50"

        # 1. Handle Cliente
        cur.execute("SELECT id_cliente FROM clientes WHERE dni = %s", (dni,))
        cliente = cur.fetchone()
        if cliente:
            id_cliente = cliente['id_cliente']
            print(f"Existing client found: {id_cliente}")
        else:
            cur.execute("""
                INSERT INTO clientes (dni, nombre, apellido) 
                VALUES (%s, %s, %s) RETURNING id_cliente
            """, (dni, nombre, apellido))
            id_cliente = cur.fetchone()['id_cliente']
            print(f"New client created: {id_cliente}")

        # 2. Handle Vehículo
        cur.execute("SELECT placa FROM vehiculos WHERE placa = %s", (placa,))
        vehiculo = cur.fetchone()
        if not vehiculo:
            cur.execute("""
                INSERT INTO vehiculos (placa, marca, modelo, kilometraje_ingreso) 
                VALUES (%s, %s, %s, %s)
            """, (placa, marca, modelo, km_actual))
            print(f"New vehicle created: {placa}")
        
        # 3. Order
        num_orden = f"TEST-{datetime.now().strftime('%M%S')}"
        cur.execute("""
            INSERT INTO ordenes_servicio 
            (numero_orden, id_cliente, placa_vehiculo, kilometraje_actual, tipo_aceite, tipo_trabajo, fecha_ingreso)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (num_orden, id_cliente, placa, km_actual, tipo_aceite, tipo_trabajo, datetime.now()))
        
        conn.commit()
        print(f"Order {num_orden} registered successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    test_registration()
