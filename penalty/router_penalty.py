import os
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .backend_penalty import (
    alternar_estado_sancion_backend,
    actualizar_sancion_backend,
    crear_sancion_backend,
    eliminar_sancion_backend,
    listar_sanciones_backend,
    obtener_sancion_backend,
)

router = APIRouter(prefix="/penalty", tags=["Sanciones"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "penalty_templates"))


class SancionCreate(BaseModel):
    estudiante_id: int
    motivo: str
    monto: float


@router.get("/vista", response_class=HTMLResponse)
async def vista_sanciones(request: Request, search: str = ""):
    search_value = search or ""
    sanciones = listar_sanciones_backend(search_value)
    context = {
        "penalties": sanciones,
        "search": search_value,
        "mode": "list",
    }
    return templates.TemplateResponse(request, "penalty.html", context)


@router.get("/edit/{sancion_id}", response_class=HTMLResponse)
async def vista_editar_sancion(request: Request, sancion_id: int):
    sancion = obtener_sancion_backend(sancion_id)
    if sancion is None:
        raise HTTPException(status_code=404, detail="Sanción no encontrada")

    context = {
        "penalty": sancion,
        "mode": "edit"
    }
    return templates.TemplateResponse(request, "penalty.html", context)


@router.get("/api/sanciones")
def api_obtener_sanciones(search: str = ""):
    return listar_sanciones_backend(search)


@router.post("/api/sanciones")
def api_crear_sancion(sancion: SancionCreate):
    return crear_sancion_backend(sancion.estudiante_id, sancion.motivo, sancion.monto)


@router.post("/penalties")
async def crear_sancion_form(
    estudiante_id: int = Form(...),
    motivo: str = Form(...),
    monto: float = Form(...),
):
    crear_sancion_backend(estudiante_id, motivo, monto)
    return RedirectResponse(url="/penalty/vista", status_code=303)


@router.post("/penalties/{sancion_id}/edit")
async def editar_sancion_form(
    sancion_id: int,
    estudiante_id: int = Form(...),
    motivo: str = Form(...),
    monto: float = Form(...),
):
    sancion = actualizar_sancion_backend(sancion_id, estudiante_id, motivo, monto)
    if sancion is None:
        raise HTTPException(status_code=404, detail="Sanción no encontrada")
    return RedirectResponse(url="/penalty/vista", status_code=303)


@router.post("/penalties/{sancion_id}/toggle-status")
async def cambiar_estado_sancion(sancion_id: int):
    sancion = alternar_estado_sancion_backend(sancion_id)
    if sancion is None:
        raise HTTPException(status_code=404, detail="Sanción no encontrada")
    return RedirectResponse(url="/penalty/vista", status_code=303)


@router.post("/penalties/{sancion_id}/delete")
async def eliminar_sancion_form(sancion_id: int):
    eliminado = eliminar_sancion_backend(sancion_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Sanción no encontrada")
    return RedirectResponse(url="/penalty/vista", status_code=303)