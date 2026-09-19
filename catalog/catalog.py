from fastapi import APIRouter, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(
    prefix="/catalog",
    tags=["Catálogo y Libros"]
)

# Modelo de datos
class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str
    isbn: str
    available: bool = True

# Base de datos temporal
catalog_db: List[Book] = [
    Book(id=1, title="Cien Años de Soledad", author="Gabriel García Márquez", category="Novela", isbn="978-0307474728", available=False),
    Book(id=2, title="Don Quijote de la Mancha", author="Miguel de Cervantes", category="Clásico", isbn="978-8424116033"),
    Book(id=3, title="El Principito", author="Antoine de Saint-Exupéry", category="Fábula", isbn="978-0156013987")
]

# --- ENDPOINTS API Y LÓGICA ---

@router.get("/books", response_model=List[Book])
def get_books(search: Optional[str] = Query(None)):
    if search:
        query = search.lower()
        return [
            b for b in catalog_db
            if query in b.title.lower() or query in b.author.lower() or query in b.category.lower()
        ]
    return catalog_db

@router.post("/books")
def create_book(title: str = Form(...), author: str = Form(...), category: str = Form(...), isbn: str = Form(...)):
    new_id = max([b.id for b in catalog_db], default=0) + 1
    new_book = Book(id=new_id, title=title, author=author, category=category, isbn=isbn)
    catalog_db.append(new_book)
    return RedirectResponse(url="/catalog/vista", status_code=303)

# Actualizar datos de un libro
@router.post("/books/{book_id}/edit")
def edit_book(book_id: int, title: str = Form(...), author: str = Form(...), category: str = Form(...), isbn: str = Form(...)):
    for book in catalog_db:
        if book.id == book_id:
            book.title = title
            book.author = author
            book.category = category
            book.isbn = isbn
            break
    return RedirectResponse(url="/catalog/vista", status_code=303)

# Alternar disponibilidad (Prestar / Devolver)
@router.post("/books/{book_id}/toggle-status")
def toggle_book_status(book_id: int):
    for book in catalog_db:
        if book.id == book_id:
            book.available = not book.available
            break
    return RedirectResponse(url="/catalog/vista", status_code=303)

# Eliminar libro del catálogo
@router.post("/books/{book_id}/delete")
def delete_book(book_id: int):
    global catalog_db
    catalog_db = [b for b in catalog_db if b.id != book_id]
    return RedirectResponse(url="/catalog/vista", status_code=303)

# --- VISTAS WEB HTML ---

@router.get("/edit/{book_id}", response_class=HTMLResponse)
def vista_editar(book_id: int):
    book = next((b for b in catalog_db if b.id == book_id), None)
    if not book:
        return RedirectResponse(url="/catalog/vista", status_code=303)
        
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Editar Libro</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #eef2f5; }}
            .card {{ background: white; padding: 25px; border-radius: 10px; max-width: 500px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            input {{ width: 95%; padding: 10px; margin: 8px 0; border-radius: 4px; border: 1px solid #ccc; }}
            button {{ padding: 10px 15px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }}
            a {{ text-decoration: none; color: #6c757d; margin-left: 10px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>✏️ Editar Libro #{book.id}</h2>
            <form method="post" action="/catalog/books/{book.id}/edit">
                <label>Título:</label>
                <input type="text" name="title" value="{book.title}" required>
                <label>Autor:</label>
                <input type="text" name="author" value="{book.author}" required>
                <label>Categoría:</label>
                <input type="text" name="category" value="{book.category}" required>
                <label>ISBN:</label>
                <input type="text" name="isbn" value="{book.isbn}" required>
                <br><br>
                <button type="submit">Guardar Cambios</button>
                <a href="/catalog/vista">Cancelar</a>
            </form>
        </div>
    </body>
    </html>
    """

@router.get("/vista", response_class=HTMLResponse)
def vista_catalogo(search: Optional[str] = None):
    books = get_books(search=search)
    
    rows = ""
    for b in books:
        status_btn = f"""
        <form method="post" action="/catalog/books/{b.id}/toggle-status" style="display:inline;">
            <button type="submit" class="btn-toggle" style="background-color: {'#ffc107' if b.available else '#17a2b8'}; color: {'#000' if b.available else '#fff'};">
                {'Cambiar a Prestado' if b.available else 'Cambiar a Disponible'}
            </button>
        </form>
        """
        edit_btn = f"""
        <a href="/catalog/edit/{b.id}" class="btn-edit" title="Editar">✏️</a>
        """
        delete_btn = f"""
        <form method="post" action="/catalog/books/{b.id}/delete" style="display:inline;">
            <button type="submit" class="btn-delete" onclick="return confirm('¿Eliminar este libro?');" title="Eliminar">🗑️</button>
        </form>
        """
        status_text = "🟢 Disponible" if b.available else "🔴 Prestado"

        rows += f"""
        <tr>
            <td>{b.id}</td>
            <td>{b.title}</td>
            <td>{b.author}</td>
            <td>{b.category}</td>
            <td>{b.isbn}</td>
            <td>{status_text}</td>
            <td>
                {status_btn}
                {edit_btn}
                {delete_btn}
            </td>
        </tr>
        """

    if not rows:
        rows = "<tr><td colspan='7' style='text-align:center;'>No se encontraron libros</td></tr>"

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Catálogo de Libros</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #eef2f5; }}
            .card {{ background: white; padding: 25px; border-radius: 10px; max-width: 1000px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #007bff; color: white; }}
            input, button {{ padding: 8px; margin: 4px; border-radius: 4px; border: 1px solid #ccc; }}
            button {{ border: none; cursor: pointer; border-radius: 4px; }}
            .btn-save {{ background-color: #28a745; color: white; }}
            .btn-toggle {{ font-size: 12px; padding: 6px 10px; }}
            .btn-edit {{ background-color: #ffc107; padding: 6px 10px; border-radius: 4px; text-decoration: none; font-size: 12px; color: black; display: inline-block; }}
            .btn-delete {{ background-color: #dc3545; font-size: 12px; padding: 6px 10px; color: white; }}
            a {{ text-decoration: none; color: #007bff; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="card">
            <a href="/">⬅ Volver al Dashboard Principal</a>
            <h1>📖 Gestión de Catálogo de Libros</h1>
            
            <form method="get" action="/catalog/vista">
                <input type="text" name="search" placeholder="Buscar por título, autor o categoría..." value="{search or ''}" style="width: 60%;">
                <button type="submit" style="background-color: #007bff; color: white;">Buscar</button>
                <a href="/catalog/vista" style="margin-left: 10px; font-weight: normal; font-size: 14px;">Limpiar búsqueda</a>
            </form>
            
            <hr>
            
            <h3>➕ Registrar Nuevo Libro</h3>
            <form method="post" action="/catalog/books">
                <input type="text" name="title" placeholder="Título" required>
                <input type="text" name="author" placeholder="Autor" required>
                <input type="text" name="category" placeholder="Categoría" required>
                <input type="text" name="isbn" placeholder="ISBN" required>
                <button type="submit" class="btn-save">Guardar Libro</button>
            </form>

            <h3>📚 Inventario de Libros</h3>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Título</th>
                        <th>Autor</th>
                        <th>Categoría</th>
                        <th>ISBN</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """