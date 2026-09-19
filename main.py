from fastapi import FastAPI

# Importar los módulos
import catalog.catalog as catalog_module
import loans.loans as loans_module
import penalty.penalty as penalty_module
import reports.reports as reports_module
import students.students as students_module
from reservations.reservations import router as reservations_router

app = FastAPI(title="Proyecto de Biblioteca")

# Función auxiliar para registrar routers independientemente del nombre de variable en cada módulo
def include_module_router(module):
    for attr_name in ["router", "app", "api_router"]:
        if hasattr(module, attr_name):
            app.include_router(getattr(module, attr_name))
            break

include_module_router(catalog_module)
include_module_router(loans_module)
include_module_router(penalty_module)
include_module_router(reports_module)
include_module_router(students_module)

# Incluir tu router de reservas
app.include_router(reservations_router)
