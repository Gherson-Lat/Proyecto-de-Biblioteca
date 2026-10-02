from typing import List, Optional
from pydantic import BaseModel


class Reporte(BaseModel):
    id: int
    titulo: str
    categoria: str
    generado_por: str
    archivado: bool = False


# Base de datos temporal en memoria
reportes_db: List[Reporte] = [
    Reporte(id=1, titulo="Reporte Mensual de Préstamos", categoria="Préstamos", generado_por="Sistema", archivado=False),
    Reporte(id=2, titulo="Estudiantes con Sanciones Activas", categoria="Sanciones", generado_por="Admin", archivado=True),
]


def listar_reportes_backend(search: Optional[str] = "") -> List[Reporte]:
    texto = (search or "").strip().lower()
    if not texto:
        return reportes_db

    resultado: List[Reporte] = []
    for rep in reportes_db:
        if (
            texto in rep.titulo.lower()
            or texto in rep.categoria.lower()
            or texto in rep.generado_por.lower()
        ):
            resultado.append(rep)
    return resultado


def obtener_reporte_backend(reporte_id: int) -> Optional[Reporte]:
    for rep in reportes_db:
        if rep.id == reporte_id:
            return rep
    return None


def crear_reporte_backend(titulo: str, categoria: str, generado_por: str) -> Reporte:
    nuevo_id = max((r.id for r in reportes_db), default=0) + 1
    reporte = Reporte(
        id=nuevo_id,
        titulo=titulo.strip(),
        categoria=categoria.strip(),
        generado_por=generado_por.strip(),
        archivado=False,
    )
    reportes_db.append(reporte)
    return reporte


def actualizar_reporte_backend(reporte_id: int, titulo: str, categoria: str, generado_por: str) -> Optional[Reporte]:
    rep = obtener_reporte_backend(reporte_id)
    if rep is None:
        return None

    rep.titulo = titulo.strip()
    rep.categoria = categoria.strip()
    rep.generado_por = generado_por.strip()
    return rep


def eliminar_reporte_backend(reporte_id: int) -> bool:
    global reportes_db
    nueva_lista = [r for r in reportes_db if r.id != reporte_id]
    if len(nueva_lista) == len(reportes_db):
        return False
    reportes_db = nueva_lista
    return True


def alternar_estado_reporte_backend(reporte_id: int) -> Optional[Reporte]:
    rep = obtener_reporte_backend(reporte_id)
    if rep is None:
        return None
    rep.archivado = not rep.archivado
    return rep