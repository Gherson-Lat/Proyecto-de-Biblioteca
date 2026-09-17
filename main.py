from fastapi import FastAPI

# Importar el router de tu módulo (penalty) y de los otros módulos existentes
from penalty.penalty import router as penalty_router
# from loans.loans import router as loans_router

app = FastAPI(
    title="Sistema de Gestión de Biblioteca",
    description="API para la gestión de préstamos, sanciones, catálogo y estudiantes",
    version="1.0.0"
)

# Registrar los routers en la aplicación principal
app.include_router(penalty_router)
# app.include_router(loans_router)

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a la API del Sistema de Biblioteca"}