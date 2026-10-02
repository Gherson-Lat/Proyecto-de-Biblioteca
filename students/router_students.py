import os
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .backend_students import (
    alternar_estado_estudiante_backend,
    actualizar_estudiante_backend,
    crear_estudiante_backend,
    eliminar_estudiante_backend,
    listar_estudiantes_backend,
    obtener_estudiante_backend,
)

router = APIRouter(prefix="/students", tags=["Estudiantes"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "students_templates"))


class EstudianteCreate(BaseModel):
    nombre: str
    carrera: str
    email: str


@router.get("/vista", response_class=HTMLResponse)
async def vista_estudiantes(request: Request, search: str = ""):
    search_value = search or ""
    estudiantes = listar_estudiantes_backend(search_value)
    context = {
        "students": estudiantes,
        "search": search_value,
        "mode": "list",
    }
    return templates.TemplateResponse(request, "students.html", context)


@router.get("/edit/{estudiante_id}", response_class=HTMLResponse)
async def vista_editar_estudiante(request: Request, estudiante_id: int):
    estudiante = obtener_estudiante_backend(estudiante_id)
    if estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    context = {
        "student": estudiante,
        "mode": "edit"
    }
    return templates.TemplateResponse(request, "students.html", context)


@router.get("/api/estudiantes")
def api_obtener_estudiantes(search: str = ""):
    return listar_estudiantes_backend(search)


@router.post("/api/estudiantes")
def api_crear_estudiante(estudiante: EstudianteCreate):
    return crear_estudiante_backend(estudiante.nombre, estudiante.carrera, estudiante.email)


@router.post("/students")
async def crear_estudiante_form(
    nombre: str = Form(...),
    carrera: str = Form(...),
    email: str = Form(...),
):
    crear_estudiante_backend(nombre, carrera, email)
    return RedirectResponse(url="/students/vista", status_code=303)


@router.post("/students/{estudiante_id}/edit")
async def editar_estudiante_form(
    estudiante_id: int,
    nombre: str = Form(...),
    carrera: str = Form(...),
    email: str = Form(...),
):
    estudiante = actualizar_estudiante_backend(estudiante_id, nombre, carrera, email)
    if estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return RedirectResponse(url="/students/vista", status_code=303)


@router.post("/students/{estudiante_id}/toggle-status")
async def cambiar_estado_estudiante(estudiante_id: int):
    estudiante = alternar_estado_estudiante_backend(estudiante_id)
    if estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return RedirectResponse(url="/students/vista", status_code=303)


@router.post("/students/{estudiante_id}/delete")
async def eliminar_estudiante_form(estudiante_id: int):
    eliminado = eliminar_estudiante_backend(estudiante_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return RedirectResponse(url="/students/vista", status_code=303)