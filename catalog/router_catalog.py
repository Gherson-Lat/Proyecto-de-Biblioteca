import os
from typing import Optional

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .backend_catalog import (
    alternar_estado_libro_backend,
    crear_libro_backend,
    eliminar_libro_backend,
    listar_libros_backend,
    obtener_libro_backend,
    actualizar_libro_backend,
)

router = APIRouter(prefix="/catalog", tags=["Catálogo"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "catalog_templates"))


class LibroCreate(BaseModel):
    title: str
    author: str
    category: str
    isbn: str


@router.get("/vista", response_class=HTMLResponse)
async def vista_catalogo(request: Request, search: str = ""):
    search_value = search or ""
    libros = listar_libros_backend(search_value)
    context = {
        "books": libros,
        "search": search_value,
        "mode": "list",
    }
    return templates.TemplateResponse(request, "catalog.html", context)


@router.get("/edit/{libro_id}", response_class=HTMLResponse)
async def vista_editar_libro(request: Request, libro_id: int):
    libro = obtener_libro_backend(libro_id)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    context = {
        "book": libro,
        "mode": "edit"
    }
    return templates.TemplateResponse(request, "catalog.html", context)


@router.get("/api/libros")
def api_obtener_libros(search: str = ""):
    return listar_libros_backend(search)


@router.post("/api/libros")
def api_crear_libro(libro: LibroCreate):
    return crear_libro_backend(libro.title, libro.author, libro.category, libro.isbn)


@router.post("/books")
async def crear_libro_form(
    title: str = Form(...),
    author: str = Form(...),
    category: str = Form(...),
    isbn: str = Form(...),
):
    crear_libro_backend(title, author, category, isbn)
    return RedirectResponse(url="/catalog/vista", status_code=303)


@router.post("/books/{libro_id}/edit")
async def editar_libro_form(
    libro_id: int,
    title: str = Form(...),
    author: str = Form(...),
    category: str = Form(...),
    isbn: str = Form(...),
):
    libro = actualizar_libro_backend(libro_id, title, author, category, isbn)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return RedirectResponse(url="/catalog/vista", status_code=303)


@router.post("/books/{libro_id}/toggle-status")
async def cambiar_estado_libro(libro_id: int):
    libro = alternar_estado_libro_backend(libro_id)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return RedirectResponse(url="/catalog/vista", status_code=303)


@router.post("/books/{libro_id}/delete")
async def eliminar_libro_form(libro_id: int):
    eliminado = eliminar_libro_backend(libro_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return RedirectResponse(url="/catalog/vista", status_code=303)