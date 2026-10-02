import os
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .backend_reports import (
    alternar_estado_reporte_backend,
    actualizar_reporte_backend,
    crear_reporte_backend,
    eliminar_reporte_backend,
    listar_reportes_backend,
    obtener_reporte_backend,
)

router = APIRouter(prefix="/reports", tags=["Reportes"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "reports_templates"))


class ReporteCreate(BaseModel):
    titulo: str
    categoria: str
    generado_por: str


@router.get("/vista", response_class=HTMLResponse)
async def vista_reportes(request: Request, search: str = ""):
    search_value = search or ""
    reportes = listar_reportes_backend(search_value)
    context = {
        "reports": reportes,
        "search": search_value,
        "mode": "list",
    }
    return templates.TemplateResponse(request, "reports.html", context)


@router.get("/edit/{reporte_id}", response_class=HTMLResponse)
async def vista_editar_reporte(request: Request, reporte_id: int):
    reporte = obtener_reporte_backend(reporte_id)
    if reporte is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    context = {
        "report": reporte,
        "mode": "edit"
    }
    return templates.TemplateResponse(request, "reports.html", context)


@router.get("/api/reportes")
def api_obtener_reportes(search: str = ""):
    return listar_reportes_backend(search)


@router.post("/api/reportes")
def api_crear_reporte(reporte: ReporteCreate):
    return crear_reporte_backend(reporte.titulo, reporte.categoria, reporte.generado_por)


@router.post("/reports")
async def crear_reporte_form(
    titulo: str = Form(...),
    categoria: str = Form(...),
    generado_por: str = Form(...),
):
    crear_reporte_backend(titulo, categoria, generado_por)
    return RedirectResponse(url="/reports/vista", status_code=303)


@router.post("/reports/{reporte_id}/edit")
async def editar_reporte_form(
    reporte_id: int,
    titulo: str = Form(...),
    categoria: str = Form(...),
    generado_por: str = Form(...),
):
    reporte = actualizar_reporte_backend(reporte_id, titulo, categoria, generado_por)
    if reporte is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return RedirectResponse(url="/reports/vista", status_code=303)


@router.post("/reports/{reporte_id}/toggle-status")
async def cambiar_estado_reporte(reporte_id: int):
    reporte = alternar_estado_reporte_backend(reporte_id)
    if reporte is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return RedirectResponse(url="/reports/vista", status_code=303)


@router.post("/reports/{reporte_id}/delete")
async def eliminar_reporte_form(reporte_id: int):
    eliminado = eliminar_reporte_backend(reporte_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return RedirectResponse(url="/reports/vista", status_code=303)