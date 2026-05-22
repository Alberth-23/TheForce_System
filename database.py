import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Tu URL de conexión (Reemplaza los datos reales)
DATABASE_URL = "postgresql://theforce:JiLchuSwX6xksmeJi8k0a13ITSH0Shov@dpg-d8190avavr4c73b6rmq0-a.virginia-postgres.render.com/theforcedb"

def get_db_connection():
    try:
        # Nos conectamos usando directamente la URL
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        print("✅ Conexión exitosa mediante URL")
        return conn
    except Exception as e:
        print(f"❌ Error conectando con URL: {e}")
        return None

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        conn.close()