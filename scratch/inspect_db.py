from database import get_db_connection

def list_db_structure():
    conn = get_db_connection()
    if not conn:
        print("Could not connect to the database.")
        return

    try:
        with conn.cursor() as cur:
            # Get all tables in the public schema
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE';
            """)
            tables = cur.fetchall()
            
            if not tables:
                print("No tables found in the 'public' schema.")
                return

            for table in tables:
                table_name = table['table_name']
                print(f"\nTable: {table_name}")
                print("-" * (7 + len(table_name)))
                
                # Get columns for each table
                cur.execute(f"""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = '{table_name}'
                    ORDER BY ordinal_position;
                """)
                columns = cur.fetchall()
                for col in columns:
                    print(f"  - {col['column_name']} ({col['data_type']}) {'NULL' if col['is_nullable'] == 'YES' else 'NOT NULL'}")
    except Exception as e:
        print(f"Error reading structure: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    list_db_structure()
