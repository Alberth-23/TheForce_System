from app.core.db import SessionLocal
from app.models.domain import Cliente, Empresa

def link_last_to_novaflat():
    db = SessionLocal()
    novaflat = db.query(Empresa).filter(Empresa.nombre_empresa == "Novaflat").first()
    if not novaflat:
        novaflat = Empresa(nombre_empresa="Novaflat")
        db.add(novaflat)
        db.flush()
    
    last_client = db.query(Cliente).order_by(Cliente.id_cliente.desc()).first()
    if last_client:
        last_client.id_empresa = novaflat.id
        db.commit()
        print(f"Vinculado cliente {last_client.nombre} {last_client.apellido} a Novaflat")
    else:
        print("No se encontró ningún cliente")
    db.close()

if __name__ == "__main__":
    link_last_to_novaflat()
