from app.core.db import engine, Base
from app.models.domain import Usuario
from sqlalchemy.orm import Session
import bcrypt

def init_db():
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")

    # Crear usuario admin por defecto si no existe
    with Session(engine) as session:
        admin_exists = session.query(Usuario).filter(Usuario.username == "admin").first()
        if not admin_exists:
            print("Creando usuario admin...")
            hashed_pw = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_admin = Usuario(
                username="admin",
                hashed_password=hashed_pw,
                full_name="Administrator",
                role="admin"
            )
            session.add(new_admin)
            session.commit()
            print("Usuario admin creado: admin / admin123")
        else:
            print("El usuario admin ya existe.")

if __name__ == "__main__":
    init_db()
