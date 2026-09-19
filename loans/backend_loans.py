from datetime import datetime, timedelta

prestamos_db = []

def registrar_prestamo_backend(estudiante_id: str, libro_id: str) -> dict:
    # Verificar si el estudiante ya tiene este mismo libro prestado
    for prestamo in prestamos_db:
        if (
            prestamo["estudiante_id"] == estudiante_id
            and prestamo["libro_id"] == libro_id
            and prestamo["estado"] == "ACTIVO"
        ):
            return {
                "error": True,
                "mensaje": "El estudiante ya tiene este libro registrado en un préstamo activo."
            }

    # Registrar nuevo préstamo
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

def devolver_prestamo_backend(id_prestamo: int) -> dict:
    # Buscar el préstamo por su ID
    for prestamo in prestamos_db:
        if prestamo["id_prestamo"] == id_prestamo:
            if prestamo["estado"] == "DEVUELTO":
                return {
                    "error": True,
                    "mensaje": "Este libro ya fue devuelto previamente."
                }
            
            prestamo["estado"] = "DEVUELTO"
            prestamo["fecha_devolucion"] = datetime.now().strftime("%Y-%m-%d")
            return {
                "error": False,
                "mensaje": "El libro ha sido devuelto con éxito."
            }
            
    return {
        "error": True,
        "mensaje": "No se encontró ningún préstamo activo con ese ID."
    }

def obtener_prestamos_activos_backend() -> list:
    return [p for p in prestamos_db if p["estado"] == "ACTIVO"]