# ==============================================================================
# MAIN GLOBAL - TABLERO CENTRAL DEL SISTEMA DE BIBLIOTECA (FastAPI)
# ==============================================================================
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Importación de los routers de cada módulo
# (Cada integrante exporta su APIRouter desde su carpeta)
from loans.router_loans import router as router_loans
from catalog.router_catalog import router as router_catalog
#from students.router_students import router as router_students
#from penalty.router_penalty import router as router_penalty
#from reports.router_reports import router as router_reports

app = FastAPI(
    title="Sistema de Gestión Bibliotecaria",
    description="Tablero Centralizador Modulado por API REST y Vistas Web",
    version="1.0.0"
)

#Integración de los routers al tablero central
app.include_router(router_loans)
app.include_router(router_catalog)
#app.include_router(router_students)
#app.include_router(router_penalty)
#app.include_router(router_reports)

@app.get("/", response_class=HTMLResponse)
def dashboard_principal():
    """Página de inicio global (Dashboard) que enlaza a los submódulos."""
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard Principal - Biblioteca</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #eef2f5; text-align: center; }
            .card-container { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 30px; }
            .card { background: white; padding: 25px; border-radius: 10px; width: 220px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            a { text-decoration: none; color: #007bff; font-weight: bold; }
            a:hover { color: #0056b3; }
        </style>
    </head>
    <body>
        <h1>📚 Dashboard Principal de la Biblioteca</h1>
        <p>Seleccione el módulo al que desea ingresar:</p>
        <div class="card-container">
            <div class="card">
                <h3>Préstamos</h3>
                <a href="/loans/vista">Ir a Préstamos ➔</a>
            </div>
            <div class="card">
                <h3>Catálogo</h3>
                <a href="/catalog/vista">Ir al Catálogo ➔</a>
            </div>
            <div class="card">
                <h3>Estudiantes</h3>
                <span>En construcción...</span>
            </div>
            <div class="card">
                <h3>Sanciones</h3>
                <span>En construcción...</span>
            </div>
            <div class="card">
                <h3>Reportes</h3>
                <span>En construcción...</span>
            </div>
        </div>
    </body>
    </html>
    """