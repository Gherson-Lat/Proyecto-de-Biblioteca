from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Inicialización del router
router = APIRouter(prefix="/catalog", tags=["Catálogo de Libros"])

# Configuración de plantillas Jinja2
templates = Jinja2Templates(directory="catalog/templates")

# ------------------------------------
# 1. RUTA PARA LA VISTA WEB (HTML)
# ------------------------------------
@router.get("/vista", response_class=HTMLResponse)
def vista_catalog(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request})

# ------------------------------------
# 2. ENDPOINTS DE LA API (CRUD)
# ------------------------------------
@router.get("/libros")
def listar_libros():
    # Tu lógica para obtener y retornar libros
    return [{"id": 1, "titulo": "Cien Años de Soledad", "autor": "Gabriel García Márquez"}]

@router.post("/libros")
def crear_libro(datos: dict):
    # Tu lógica para guardar un libro
    return {"mensaje": "Libro creado con éxito", "datos": datos}