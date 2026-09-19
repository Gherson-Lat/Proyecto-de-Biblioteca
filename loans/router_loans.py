from datetime import date
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Form, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from . import backend_loans

# Ajusta este import si el paquete "catalog" no está un nivel arriba de "loans/"
from catalog import backend_catalog

router = APIRouter(
    prefix="/loans",
    tags=["Préstamos"],
)

TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# --- ENDPOINTS API (JSON / acciones) ---

@router.get("/records")
def api_get_loans(search: Optional[str] = Query(None)):
    return backend_loans.get_loans(search=search)


@router.post("/records")
def api_create_loan(
    book_id: int = Form(...),
    borrower_name: str = Form(...),
    borrower_document: str = Form(...),
    due_date: str = Form(...),
):
    book = backend_catalog.obtener_libro_backend(book_id)
    # Si el libro no existe o ya está prestado, no se crea el préstamo
    if not book:
        raise HTTPException(status_code=404, detail="El libro no existe.")
    if not book.available:
        raise HTTPException(status_code=409, detail="El libro no está disponible.")

    try:
        backend_loans.create_loan(book_id, book.title, borrower_name, borrower_document, due_date)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    backend_catalog.alternar_estado_libro_backend(book_id)  # queda como "Prestado"
    return RedirectResponse(url="/loans/vista", status_code=303)


@router.post("/{loan_id}/edit")
def api_edit_loan(
    loan_id: int,
    borrower_name: str = Form(...),
    borrower_document: str = Form(...),
    due_date: str = Form(...),
):
    try:
        updated_loan = backend_loans.update_loan(
            loan_id, borrower_name, borrower_document, due_date
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if not updated_loan:
        raise HTTPException(status_code=404, detail="El préstamo no existe.")
    return RedirectResponse(url="/loans/vista", status_code=303)


@router.post("/{loan_id}/return")
def api_return_loan(loan_id: int):
    loan = backend_loans.get_loan_by_id(loan_id)
    if loan and loan["status"] == "Activo":
        backend_loans.return_loan(loan_id)
        book = backend_catalog.obtener_libro_backend(loan["book_id"])
        if book and not book.available:
            backend_catalog.alternar_estado_libro_backend(loan["book_id"])  # vuelve a "Disponible"
    return RedirectResponse(url="/loans/vista", status_code=303)


@router.post("/{loan_id}/delete")
def api_delete_loan(loan_id: int):
    loan = backend_loans.get_loan_by_id(loan_id)
    # Si se borra un préstamo activo, liberamos el libro en el catálogo
    if loan and loan["status"] == "Activo":
        book = backend_catalog.obtener_libro_backend(loan["book_id"])
        if book and not book.available:
            backend_catalog.alternar_estado_libro_backend(loan["book_id"])
    backend_loans.delete_loan(loan_id)
    return RedirectResponse(url="/loans/vista", status_code=303)


# --- VISTAS WEB (un único template: loans.html) ---

@router.get("/vista")
def vista_prestamos(request: Request, search: Optional[str] = None):
    loans = backend_loans.get_loans(search=search)
    active_book_ids = backend_loans.get_active_book_ids()
    available_books = [
        b for b in backend_catalog.listar_libros_backend()
        if b.available and b.id not in active_book_ids
    ]
    return templates.TemplateResponse(
        "loans_view.html",
        {
            "request": request,
            "loans": loans,
            "search": search or "",
            "available_books": available_books,
            "editing_loan": None,
            "today": date.today().isoformat(),
        },
    )


@router.get("/edit/{loan_id}")
def vista_editar_prestamo(request: Request, loan_id: int):
    loan = backend_loans.get_loan_by_id(loan_id)
    if not loan:
        return RedirectResponse(url="/loans/vista", status_code=303)

    return templates.TemplateResponse(
        "loans_view.html",
        {
            "request": request,
            "loans": [],
            "search": "",
            "available_books": [],
            "editing_loan": loan,
            "today": date.today().isoformat(),
        },
    )