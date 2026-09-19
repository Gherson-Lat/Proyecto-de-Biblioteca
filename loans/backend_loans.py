import sqlite3
from datetime import date
from pathlib import Path
from typing import List, Optional

# Base de datos SQLite dedicada a este módulo (se crea junto a este archivo)
DB_PATH = Path(__file__).parent / "loans.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row  # permite acceder a columnas por nombre
    return conn


def init_db() -> None:
    """Crea la tabla de préstamos si no existe."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                book_title TEXT NOT NULL,
                borrower_name TEXT NOT NULL,
                borrower_document TEXT NOT NULL,
                loan_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                return_date TEXT,
                status TEXT NOT NULL DEFAULT 'Activo'
                    CHECK (status IN ('Activo', 'Devuelto'))
            )
            """
        )
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS one_active_loan_per_book
            ON loans (book_id) WHERE status = 'Activo'
            """
        )


# Se asegura de que la tabla exista al importar el módulo
init_db()


def _row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)


def get_loans(search: Optional[str] = None) -> List[dict]:
    with get_connection() as conn:
        if search and search.strip():
            q = f"%{search.strip().lower()}%"
            rows = conn.execute(
                """
                SELECT * FROM loans
                WHERE lower(book_title) LIKE ?
                   OR lower(borrower_name) LIKE ?
                   OR lower(borrower_document) LIKE ?
                ORDER BY id DESC
                """,
                (q, q, q),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM loans ORDER BY id DESC").fetchall()
    return [_row_to_dict(r) for r in rows]


def get_loan_by_id(loan_id: int) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
    return _row_to_dict(row) if row else None


def get_active_book_ids() -> set[int]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT book_id FROM loans WHERE status = 'Activo'"
        ).fetchall()
    return {row["book_id"] for row in rows}


def create_loan(
    book_id: int, book_title: str, borrower_name: str, borrower_document: str, due_date: str
) -> dict:
    loan_date = date.today().isoformat()
    due_date = _validate_loan_data(book_title, borrower_name, borrower_document, due_date, loan_date)
    with get_connection() as conn:
        try:
            cur = conn.execute(
                """
                INSERT INTO loans (book_id, book_title, borrower_name, borrower_document, loan_date, due_date, status)
                VALUES (?, ?, ?, ?, ?, ?, 'Activo')
                """,
                (book_id, book_title.strip(), borrower_name.strip(), borrower_document.strip(), loan_date, due_date),
            )
        except sqlite3.IntegrityError as error:
            raise ValueError("El libro ya tiene un préstamo activo.") from error
        new_id = cur.lastrowid
    return get_loan_by_id(new_id)


def update_loan(loan_id: int, borrower_name: str, borrower_document: str, due_date: str) -> Optional[dict]:
    loan = get_loan_by_id(loan_id)
    if not loan:
        return None
    due_date = _validate_loan_data(
        loan["book_title"], borrower_name, borrower_document, due_date, loan["loan_date"]
    )
    with get_connection() as conn:
        conn.execute(
            "UPDATE loans SET borrower_name = ?, borrower_document = ?, due_date = ? WHERE id = ?",
            (borrower_name.strip(), borrower_document.strip(), due_date, loan_id),
        )
    return get_loan_by_id(loan_id)


def return_loan(loan_id: int) -> Optional[dict]:
    with get_connection() as conn:
        conn.execute(
            "UPDATE loans SET status = 'Devuelto', return_date = ? WHERE id = ? AND status = 'Activo'",
            (date.today().isoformat(), loan_id),
        )
    return get_loan_by_id(loan_id)


def delete_loan(loan_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM loans WHERE id = ?", (loan_id,))
        deleted = cur.rowcount > 0
    return deleted


def _validate_loan_data(
    book_title: str,
    borrower_name: str,
    borrower_document: str,
    due_date: str,
    loan_date: str,
) -> str:
    if not book_title.strip() or not borrower_name.strip() or not borrower_document.strip():
        raise ValueError("El libro y los datos del prestatario son obligatorios.")

    try:
        due = date.fromisoformat(due_date)
        loan = date.fromisoformat(loan_date)
    except (TypeError, ValueError) as error:
        raise ValueError("La fecha de vencimiento no es válida.") from error

    if due < loan:
        raise ValueError("La fecha de vencimiento no puede ser anterior al préstamo.")
    return due.isoformat()