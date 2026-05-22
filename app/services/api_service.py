import requests

def buscar_dni(dni: str):
    # NOTA: Aquí se integraría la API de tu preferencia (ej. apis.net.pe, apiperu.dev)
    # Por ahora, simularemos la respuesta para que veas el funcionamiento en el frontend
    
    # Simulación de respuesta exitosa
    mock_data = {
        "70654321": {"nombre": "JUAN CARLOS", "apellido": "PEREZ LOPEZ"},
        "12345678": {"nombre": "MARIA ELENA", "apellido": "GARCIA RUIZ"}
    }
    
    if dni in mock_data:
        return {"success": True, "data": mock_data[dni]}
    
    # Si no está en el mock, podrías llamar a la API real aquí:
    # res = requests.get(f"https://api.apis.net.pe/v1/dni?numero={dni}")
    # return res.json()
    
    return {"success": False, "message": "No encontrado en base de datos"}
