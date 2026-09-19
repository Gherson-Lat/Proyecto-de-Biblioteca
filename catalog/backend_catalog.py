from typing import List, Optional
from pydantic import BaseModel


class Libro(BaseModel):
    id: int
    title: str
    author: str
    category: str
    isbn: str
    available: bool = True


# Base de datos temporal en memoria
libros_db: List[Libro] = [
    Libro(id=1, title="Cien años de soledad", author="Gabriel García Márquez", category="Realismo mágico", isbn="978-0307474728", available=True),
    Libro(id=2, title="Don Quijote de la Mancha", author="Miguel de Cervantes", category="Clásico", isbn="978-8420412146", available=False),
    Libro(id=3, title="Harry Potter y la piedra filosofal", author="J.K. Rowling", category="Fantasía", isbn="978-8478884450", available=True),
]


def listar_libros_backend(search: Optional[str] = "") -> List[Libro]:
    texto = (search or "").strip().lower()
    if not texto:
        return libros_db

    resultado: List[Libro] = []
    for libro in libros_db:
        if (
            texto in libro.title.lower()
            or texto in libro.author.lower()
            or texto in libro.category.lower()
            or texto in libro.isbn.lower()
        ):
            resultado.append(libro)
    return resultado


def obtener_libro_backend(libro_id: int) -> Optional[Libro]:
    for libro in libros_db:
        if libro.id == libro_id:
            return libro
    return None


def crear_libro_backend(title: str, author: str, category: str, isbn: str) -> Libro:
    nuevo_id = max((libro.id for libro in libros_db), default=0) + 1
    libro = Libro(
        id=nuevo_id,
        title=title.strip(),
        author=author.strip(),
        category=category.strip(),
        isbn=isbn.strip(),
        available=True,
    )
    libros_db.append(libro)
    return libro


def actualizar_libro_backend(libro_id: int, title: str, author: str, category: str, isbn: str) -> Optional[Libro]:
    libro = obtener_libro_backend(libro_id)
    if libro is None:
        return None

    libro.title = title.strip()
    libro.author = author.strip()
    libro.category = category.strip()
    libro.isbn = isbn.strip()
    return libro


def eliminar_libro_backend(libro_id: int) -> bool:
    global libros_db
    nueva_lista = [libro for libro in libros_db if libro.id != libro_id]
    if len(nueva_lista) == len(libros_db):
        return False
    libros_db = nueva_lista
    return True


def alternar_estado_libro_backend(libro_id: int) -> Optional[Libro]:
    libro = obtener_libro_backend(libro_id)
    if libro is None:
        return None
    libro.available = not libro.available
    return libro


def buscar_libros_backend(search: str = "") -> List[Libro]:
    return listar_libros_backend(search)