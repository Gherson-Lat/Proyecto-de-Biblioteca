from typing import List, Optional
from pydantic import BaseModel


class Sancion(BaseModel):
    id: int
    estudiante_id: int
    motivo: str
    monto: float
    resuelta: bool = False


# Base de datos temporal en memoria
sanciones_db: List[Sancion] = [
    Sancion(id=1, estudiante_id=1, motivo="Devolución con retraso", monto=15.50, resuelta=False),
    Sancion(id=2, estudiante_id=2, motivo="Libro dañado", monto=50.00, resuelta=True),
]


def listar_sanciones_backend(search: Optional[str] = "") -> List[Sancion]:
    texto = (search or "").strip().lower()
    if not texto:
        return sanciones_db

    resultado: List[Sancion] = []
    for sancion in sanciones_db:
        if (
            texto in str(sancion.estudiante_id)
            or texto in sancion.motivo.lower()
        ):
            resultado.append(sancion)
    return resultado


def obtener_sancion_backend(sancion_id: int) -> Optional[Sancion]:
    for sancion in sanciones_db:
        if sancion.id == sancion_id:
            return sancion
    return None


def crear_sancion_backend(estudiante_id: int, motivo: str, monto: float) -> Sancion:
    nuevo_id = max((s.id for s in sanciones_db), default=0) + 1
    sancion = Sancion(
        id=nuevo_id,
        estudiante_id=estudiante_id,
        motivo=motivo.strip(),
        monto=monto,
        resuelta=False,
    )
    sanciones_db.append(sancion)
    return sancion


def actualizar_sancion_backend(sancion_id: int, estudiante_id: int, motivo: str, monto: float) -> Optional[Sancion]:
    sancion = obtener_sancion_backend(sancion_id)
    if sancion is None:
        return None

    sancion.estudiante_id = estudiante_id
    sancion.motivo = motivo.strip()
    sancion.monto = monto
    return sancion


def eliminar_sancion_backend(sancion_id: int) -> bool:
    global sanciones_db
    nueva_lista = [s for s in sanciones_db if s.id != sancion_id]
    if len(nueva_lista) == len(sanciones_db):
        return False
    sanciones_db = nueva_lista
    return True


def alternar_estado_sancion_backend(sancion_id: int) -> Optional[Sancion]:
    sancion = obtener_sancion_backend(sancion_id)
    if sancion is None:
        return None
    sancion.resuelta = not sancion.resuelta
    return sancion