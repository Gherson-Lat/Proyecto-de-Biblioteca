from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional

router = APIRouter(prefix="/reservations", tags=["Reservas"])

# Base de datos simulada en memoria con URLs de portadas de libros
db_reservations = [
    {
        "id": 1,
        "student": "Juan Pérez",
        "book": "Cien años de soledad",
        "cover": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1327881361i/32993.jpg",
        "date": "2026-03-20",
        "status": "Activa"
    },
    {
        "id": 2,
        "student": "María López",
        "book": "Don Quijote de la Mancha",
        "cover": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1546112331i/3836.jpg",
        "date": "2026-03-21",
        "status": "Cancelada"
    },
    {
        "id": 3,
        "student": "Carlos Ruiz",
        "book": "Harry Potter y la piedra filosofal",
        "cover": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1550337333i/7235533.jpg",
        "date": "2026-03-22",
        "status": "Activa"
    },
]

COVER_DEFAULT = "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=300&q=80"

# --- VISTA WEB PRINCIPAL CON FONDO DE BIBLIOTECA ---
@router.get("/vista", response_class=HTMLResponse, summary="Vista Web de Reservas")
def vista_reservas(q: Optional[str] = None):
    filtered_db = db_reservations
    if q:
        q_lower = q.lower()
        filtered_db = [
            r for r in db_reservations 
            if q_lower in r["student"].lower() or q_lower in r["book"].lower()
        ]

    rows = ""
    for r in filtered_db:
        is_active = r["status"] == "Activa"
        badge_style = "background: #e6f4ea; color: #137333; border: 1px solid #ceead6;" if is_active else "background: #fce8e6; color: #c5221f; border: 1px solid #fad2cf;"
        
        # Botón de Estado (Activar/Cancelar)
        if is_active:
            status_btn = f"""
            <form action="/reservations/toggle-status/{r['id']}" method="post" style="display:inline;">
                <button type="submit" class="btn-action btn-warning" title="Cancelar Reserva">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg> Cancelar
                </button>
            </form>
            """
        else:
            status_btn = f"""
            <form action="/reservations/toggle-status/{r['id']}" method="post" style="display:inline;">
                <button type="submit" class="btn-action btn-info" title="Reactivar Reserva">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 4v6h6M23 20v-6h-6"/><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/></svg> Reactivar
                </button>
            </form>
            """

        rows += f"""
        <tr>
            <td><strong>#{r['id']}</strong></td>
            <td>
                <div class="book-info">
                    <img src="{r.get('cover', COVER_DEFAULT)}" alt="Portada" class="book-cover" onerror="this.src='{COVER_DEFAULT}';">
                    <div>
                        <div class="book-title">{r['book']}</div>
                    </div>
                </div>
            </td>
            <td>
                <div class="user-chip">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                    {r['student']}
                </div>
            </td>
            <td>
                <span class="date-tag">📅 {r['date']}</span>
            </td>
            <td>
                <span class="status-pill" style="{badge_style}">
                    ● {r['status']}
                </span>
            </td>
            <td>
                <div class="actions-wrapper">
                    {status_btn}
                    <a href="/reservations/edit/{r['id']}" class="btn-action btn-primary" title="Editar">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                    </a>
                    <form action="/reservations/delete/{r['id']}" method="post" style="display:inline;" onsubmit="return confirm('¿Eliminar la reserva permanentemente?');">
                        <button type="submit" class="btn-action btn-danger" title="Eliminar">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                        </button>
                    </form>
                </div>
            </td>
        </tr>
        """

    search_val = q if q else ""

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Gestión de Reservas - Biblioteca</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
            body {{
                background: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.75)), 
                            url('https://images.unsplash.com/photo-1521587760476-6c12a4b040da?q=80&w=1920&auto=format&fit=crop');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                padding: 40px 20px;
            }}
            .main-card {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(12px);
                border-radius: 16px;
                width: 100%;
                max-width: 1050px;
                padding: 35px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            }}
            .header-nav {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }}
            .back-link {{
                text-decoration: none; color: #2563eb; font-weight: 600; font-size: 14px;
                display: inline-flex; align-items: center; gap: 6px; background: #eff6ff; padding: 8px 14px; border-radius: 8px;
            }}
            .back-link:hover {{ background: #dbeafe; }}
            h2 {{ color: #0f172a; font-size: 26px; font-weight: 700; display: flex; align-items: center; gap: 10px; }}
            
            .search-section {{ margin-bottom: 25px; }}
            .search-bar {{ display: flex; gap: 10px; }}
            .search-bar input, .form-inline input {{
                padding: 11px 16px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; outline: none; transition: all 0.2s;
            }}
            .search-bar input:focus, .form-inline input:focus {{ border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15); }}
            
            .btn {{
                padding: 11px 18px; border: none; border-radius: 8px; font-weight: 600; font-size: 14px; cursor: pointer;
                display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s; text-decoration: none;
            }}
            .btn-main {{ background: #2563eb; color: white; }}
            .btn-main:hover {{ background: #1d4ed8; }}
            .btn-success {{ background: #16a34a; color: white; }}
            .btn-success:hover {{ background: #15803d; }}

            .form-box {{
                background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 30px;
            }}
            .form-box h3 {{ font-size: 16px; color: #334155; margin-bottom: 12px; font-weight: 600; }}
            .form-inline {{ display: flex; gap: 10px; flex-wrap: wrap; }}
            .form-inline input {{ flex: 1; min-width: 180px; background: white; }}

            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th {{ background: #f1f5f9; color: #475569; text-align: left; padding: 14px; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
            td {{ padding: 14px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; color: #334155; font-size: 14px; }}
            tr:hover {{ background: #f8fafc; }}

            .book-info {{ display: flex; align-items: center; gap: 12px; }}
            .book-cover {{ width: 42px; height: 60px; object-fit: cover; border-radius: 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.15); }}
            .book-title {{ font-weight: 600; color: #0f172a; font-size: 14px; }}
            
            .user-chip {{ display: inline-flex; align-items: center; gap: 6px; background: #f1f5f9; padding: 6px 10px; border-radius: 20px; font-weight: 500; font-size: 13px; color: #475569; }}
            .date-tag {{ font-size: 13px; color: #64748b; font-weight: 500; }}
            .status-pill {{ padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }}

            .actions-wrapper {{ display: flex; gap: 6px; align-items: center; }}
            .btn-action {{
                padding: 6px 10px; border-radius: 6px; border: none; font-size: 12px; font-weight: 600; cursor: pointer;
                display: inline-flex; align-items: center; gap: 4px; text-decoration: none;
            }}
            .btn-warning {{ background: #fef3c7; color: #b45309; }}
            .btn-warning:hover {{ background: #fde68a; }}
            .btn-info {{ background: #e0f2fe; color: #0369a1; }}
            .btn-info:hover {{ background: #bae6fd; }}
            .btn-primary {{ background: #eff6ff; color: #2563eb; }}
            .btn-primary:hover {{ background: #dbeafe; }}
            .btn-danger {{ background: #fee2e2; color: #dc2626; }}
            .btn-danger:hover {{ background: #fca5a5; }}
        </style>
    </head>
    <body>
        <div class="main-card">
            <div class="header-nav">
                <h2>📚 Gestión de Reservas de Libros</h2>
                <a href="/" class="back-link">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                    Dashboard Principal
                </a>
            </div>

            <!-- Búsqueda -->
            <div class="search-section">
                <form action="/reservations/vista" method="get" class="search-bar">
                    <input type="text" name="q" value="{search_val}" placeholder="Buscar por estudiante o libro..." style="flex:1;">
                    <button type="submit" class="btn btn-main">Buscar</button>
                    <a href="/reservations/vista" class="btn" style="background:#e2e8f0; color:#475569;">Limpiar</a>
                </form>
            </div>

            <!-- Formulario para agregar -->
            <div class="form-box">
                <h3>➕ Registrar Nueva Reserva</h3>
                <form action="/reservations/create-form" method="post" class="form-inline">
                    <input type="text" name="student" placeholder="Nombre del Estudiante" required>
                    <input type="text" name="book" placeholder="Título del Libro" required>
                    <input type="url" name="cover" placeholder="URL Carátula (opcional)">
                    <input type="date" name="date" required>
                    <button type="submit" class="btn btn-success">Guardar Reserva</button>
                </form>
            </div>

            <!-- Tabla de Reservas -->
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Libro</th>
                        <th>Estudiante</th>
                        <th>Fecha Reserva</th>
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

# --- VISTA DE EDICIÓN ESTILIZADA ---
@router.get("/edit/{reservation_id}", response_class=HTMLResponse)
def vista_editar_reserva(reservation_id: int):
    res = next((r for r in db_reservations if r["id"] == reservation_id), None)
    if not res:
        return RedirectResponse(url="/reservations/vista", status_code=303)

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Editar Reserva #{res['id']}</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
            body {{
                background: linear-gradient(rgba(15, 23, 42, 0.8), rgba(15, 23, 42, 0.8)), 
                            url('https://images.unsplash.com/photo-1521587760476-6c12a4b040da?q=80&w=1920&auto=format&fit=crop');
                background-size: cover; background-position: center; min-height: 100vh;
                display: flex; justify-content: center; align-items: center; padding: 20px;
            }}
            .card {{
                background: white; border-radius: 16px; width: 100%; max-width: 480px; padding: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            }}
            h2 {{ font-size: 20px; color: #0f172a; margin-bottom: 20px; display: flex; align-items: center; gap: 8px; }}
            label {{ font-size: 13px; font-weight: 600; color: #475569; display: block; margin-bottom: 6px; }}
            input {{
                width: 100%; padding: 10px 14px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; margin-bottom: 16px; outline: none;
            }}
            input:focus {{ border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15); }}
            .btn-submit {{
                width: 100%; background: #2563eb; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 600; cursor: pointer;
            }}
            .btn-submit:hover {{ background: #1d4ed8; }}
            .back-link {{ text-decoration: none; color: #64748b; font-size: 13px; font-weight: 500; display: inline-block; margin-bottom: 15px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <a href="/reservations/vista" class="back-link">← Volver a Reservas</a>
            <h2>✏️ Editar Reserva #{res['id']}</h2>
            <form action="/reservations/update/{res['id']}" method="post">
                <label>Estudiante:</label>
                <input type="text" name="student" value="{res['student']}" required>
                <label>Libro:</label>
                <input type="text" name="book" value="{res['book']}" required>
                <label>URL Carátula:</label>
                <input type="url" name="cover" value="{res.get('cover', '')}">
                <label>Fecha de Reserva:</label>
                <input type="date" name="date" value="{res['date']}" required>
                <button type="submit" class="btn-submit">Guardar Cambios</button>
            </form>
        </div>
    </body>
    </html>
    """

# --- RUTAS DE PROCESAMIENTO ---
@router.post("/create-form", response_class=RedirectResponse)
def create_reservation_form(student: str = Form(...), book: str = Form(...), date: str = Form(...), cover: Optional[str] = Form(None)):
    new_id = len(db_reservations) + 1
    cover_img = cover if cover and cover.strip() != "" else COVER_DEFAULT
    db_reservations.append({"id": new_id, "student": student, "book": book, "cover": cover_img, "date": date, "status": "Activa"})
    return RedirectResponse(url="/reservations/vista", status_code=303)

@router.post("/update/{reservation_id}", response_class=RedirectResponse)
def update_reservation_form(reservation_id: int, student: str = Form(...), book: str = Form(...), date: str = Form(...), cover: Optional[str] = Form(None)):
    for r in db_reservations:
        if r["id"] == reservation_id:
            r["student"] = student
            r["book"] = book
            r["date"] = date
            if cover and cover.strip() != "":
                r["cover"] = cover
            break
    return RedirectResponse(url="/reservations/vista", status_code=303)

@router.post("/toggle-status/{reservation_id}", response_class=RedirectResponse)
def toggle_status_form(reservation_id: int):
    for r in db_reservations:
        if r["id"] == reservation_id:
            r["status"] = "Cancelada" if r["status"] == "Activa" else "Activa"
            break
    return RedirectResponse(url="/reservations/vista", status_code=303)

@router.post("/delete/{reservation_id}", response_class=RedirectResponse)
def delete_reservation_form(reservation_id: int):
    global db_reservations
    db_reservations = [r for r in db_reservations if r["id"] != reservation_id]
    return RedirectResponse(url="/reservations/vista", status_code=303)
