from typing import List, Optional
from pydantic import BaseModel


class Estudiante(BaseModel):
    id: int
    nombre: str
    carrera: str
    email: str
    activo: bool = True


# Base de datos temporal en memoria
estudiantes_db: List[Estudiante] = [
    Estudiante(id=1, nombre="Carlos Pérez", carrera="Ingeniería de Sistemas", email="carlos@example.com", activo=True),
    Estudiante(id=2, nombre="María López", carrera="Medicina", email="maria@example.com", activo=True),
    Estudiante(id=3, nombre="Juan Gómez", carrera="Derecho", email="juan@example.com", activo=False),
]


def listar_estudiantes_backend(search: Optional[str] = "") -> List[Estudiante]:
    texto = (search or "").strip().lower()
    if not texto:
        return estudiantes_db

    resultado: List[Estudiante] = []
    for est in estudiantes_db:
        if (
            texto in est.nombre.lower()
            or texto in est.carrera.lower()
            or texto in est.email.lower()
        ):
            resultado.append(est)
    return resultado


def obtener_estudiante_backend(estudiante_id: int) -> Optional[Estudiante]:
    for est in estudiantes_db:
        if est.id == estudiante_id:
            return est
    return None


def crear_estudiante_backend(nombre: str, carrera: str, email: str) -> Estudiante:
    nuevo_id = max((e.id for e in estudiantes_db), default=0) + 1
    estudiante = Estudiante(
        id=nuevo_id,
        nombre=nombre.strip(),
        carrera=carrera.strip(),
        email=email.strip(),
        activo=True,
    )
    estudiantes_db.append(estudiante)
    return estudiante


def actualizar_estudiante_backend(estudiante_id: int, nombre: str, carrera: str, email: str) -> Optional[Estudiante]:
    est = obtener_estudiante_backend(estudiante_id)
    if est is None:
        return None

    est.nombre = nombre.strip()
    est.carrera = carrera.strip()
    est.email = email.strip()
    return est


def eliminar_estudiante_backend(estudiante_id: int) -> bool:
    global estudiantes_db
    nueva_lista = [e for e in estudiantes_db if e.id != estudiante_id]
    if len(nueva_lista) == len(estudiantes_db):
        return False
    estudiantes_db = nueva_lista
    return True


def alternar_estado_estudiante_backend(estudiante_id: int) -> Optional[Estudiante]:
    est = obtener_estudiante_backend(estudiante_id)
    if est is None:
        return None
    est.activo = not est.activo
    return est