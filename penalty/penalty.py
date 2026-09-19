from fastapi import APIRouter

router = APIRouter(prefix="/penalty", tags=["penalty"])

# Lista temporal en memoria para almacenar el historial
historial_sanciones = []

@router.post("/agregar")
def agregar_sancion(estudiante: str, motivo: str, dias_mora: int):
    # Cálculo de ejemplo
    puntos = dias_mora * 2
    sancion = {
        "estudiante": estudiante,
        "motivo": motivo,
        "dias_mora": dias_mora,
        "puntos": puntos
    }
    historial_sanciones.append(sancion)
    return {"mensaje": "Sanción registrada con éxito", "sancion": sancion}

@router.get("/historial")
def obtener_historial():
    return {"historial": historial_sanciones}