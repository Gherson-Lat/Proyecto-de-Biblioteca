from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os

from .backend_loans import registrar_prestamo_backend, obtener_prestamos_activos_backend

router = APIRouter(prefix="/loans", tags=["Préstamos y Devoluciones"])

# Ruta absoluta para localizar la carpeta de plantillas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

class PrestamoSchema(BaseModel):
    estudiante_id: str
    libro_id: str

# Vista web (Interfaz HTML)
@router.get("/vista", response_class=HTMLResponse)
def render_vista_loans(request: Request):
    return templates.TemplateResponse("loans_view.html", {"request": request})

# Endpoints API (Consumidos por el JS del HTML)
@router.post("/api/registrar")
def api_registrar_prestamo(datos: PrestamoSchema):
    resultado = registrar_prestamo_backend(datos.estudiante_id, datos.libro_id)
    return {"status": "success", "data": resultado}

@router.get("/api/activos")
def api_obtener_activos():
    return {"activos": obtener_prestamos_activos_backend()}