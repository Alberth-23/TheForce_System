from app.core.db import SessionLocal
from app.models.domain import Usuario
import bcrypt

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def init_db():
    db = SessionLocal()
    admin = db.query(Usuario).filter(Usuario.username == "admin").first()
    if not admin:
        admin = Usuario(
            username="admin",
            hashed_password=hash_password("admin123"),
            full_name="Admin TheForce",
            role="admin"
        )
        db.add(admin)
        db.commit()
        print("Admin user created (admin / admin123)")
    else:
        print("Admin user already exists")
    db.close()

if __name__ == "__main__":
    init_db()
