from datetime import datetime, timedelta

prestamos_db = []

def registrar_prestamo_backend(estudiante_id: str, libro_id: str) -> dict:
    fecha_prestamo = datetime.now()
    fecha_limite = fecha_prestamo + timedelta(days=8)
    
    nuevo_prestamo = {
        "id_prestamo": len(prestamos_db) + 1,
        "estudiante_id": estudiante_id,
        "libro_id": libro_id,
        "fecha_prestamo": fecha_prestamo.strftime("%Y-%m-%d"),
        "fecha_limite": fecha_limite.strftime("%Y-%m-%d"),
        "estado": "ACTIVO"
    }
    prestamos_db.append(nuevo_prestamo)
    return nuevo_prestamo

def obtener_prestamos_activos_backend() -> list:
    return [p for p in prestamos_db if p["estado"] == "ACTIVO"]