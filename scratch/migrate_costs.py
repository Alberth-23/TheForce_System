from sqlalchemy import text
from app.core.db import engine

def add_cost_columns():
    with engine.connect() as conn:
        print("Añadiendo columnas de costos a la base de datos...")
        try:
            conn.execute(text("ALTER TABLE ordenes_servicio ADD COLUMN costo_mano_obra FLOAT DEFAULT 0.0"))
            conn.execute(text("ALTER TABLE ordenes_servicio ADD COLUMN costo_repuestos FLOAT DEFAULT 0.0"))
            conn.execute(text("ALTER TABLE ordenes_servicio ADD COLUMN total_pagar FLOAT DEFAULT 0.0"))
            conn.commit()
            print("Columnas añadidas con éxito.")
        except Exception as e:
            print(f"Error o columnas ya existen: {e}")

if __name__ == "__main__":
    add_cost_columns()
