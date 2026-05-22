from app.core.db import engine, Base
from app.models.domain import MovimientoInventario

def create_movimientos_table():
    print("Creando tabla de movimientos_inventario...")
    try:
        MovimientoInventario.__table__.create(engine)
        print("Tabla 'movimientos_inventario' creada con éxito.")
    except Exception as e:
        print(f"Error o tabla ya existe: {e}")

if __name__ == "__main__":
    create_movimientos_table()
