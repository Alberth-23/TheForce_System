from app.core.db import engine, Base
from app.models.domain import OrdenRepuesto

def create_orden_repuestos_table():
    print("Creando tabla de orden_repuestos...")
    try:
        OrdenRepuesto.__table__.create(engine)
        print("Tabla 'orden_repuestos' creada con éxito.")
    except Exception as e:
        print(f"Error o tabla ya existe: {e}")

if __name__ == "__main__":
    create_orden_repuestos_table()
