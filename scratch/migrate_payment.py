from sqlalchemy import text
from app.core.db import engine

def add_payment_method():
    with engine.connect() as conn:
        print("Añadiendo columna metodo_pago...")
        try:
            conn.execute(text("ALTER TABLE ordenes_servicio ADD COLUMN metodo_pago VARCHAR(50)"))
            conn.commit()
            print("Columna añadida con éxito.")
        except Exception as e:
            print(f"Error o columna ya existe: {e}")

if __name__ == "__main__":
    add_payment_method()
