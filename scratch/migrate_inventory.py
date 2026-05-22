from app.core.db import engine, Base
from app.models.domain import Producto

def create_inventory_table():
    print("Creando tabla de productos...")
    try:
        Producto.__table__.create(engine)
        print("Tabla 'productos' creada con éxito.")
    except Exception as e:
        print(f"Error o tabla ya existe: {e}")

if __name__ == "__main__":
    create_inventory_table()
