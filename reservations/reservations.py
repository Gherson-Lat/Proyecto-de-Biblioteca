from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter(prefix="/reservations", tags=["Reservas de Libros"])

# --- Modelos Pydantic ---
class ReservationCreate(BaseModel):
    student_id: int
    book_id: int

class ReservationResponse(BaseModel):
    id: int
    student_id: int
    book_id: int
    fecha_reserva: str
    estado: str  # "Pendiente", "Atendida", "Cancelada"

# Base de datos simulada en memoria
reservations_db = []

# --- Función 1: Crear una Reserva de Libro ---
@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def crear_reserva(reserva: ReservationCreate):
    """
    Permite a un estudiante reservar un libro que no está disponible temporalmente.
    """
    for r in reservations_db:
        if r["student_id"] == reserva.student_id and r["book_id"] == reserva.book_id and r["estado"] == "Pendiente":
            raise HTTPException(
                status_code=400,
                detail="El estudiante ya tiene una reserva pendiente para este libro."
            )
    
    nueva_reserva = {
        "id": len(reservations_db) + 1,
        "student_id": reserva.student_id,
        "book_id": reserva.book_id,
        "fecha_reserva": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estado": "Pendiente"
    }
    
    reservations_db.append(nueva_reserva)
    return nueva_reserva

# --- Función 2: Cancelar una Reserva ---
@router.put("/{reservation_id}/cancel", response_model=ReservationResponse)
def cancelar_reserva(reservation_id: int):
    """
    Permite cancelar una reserva previamente registrada.
    """
    for r in reservations_db:
        if r["id"] == reservation_id:
            if r["estado"] == "Cancelada":
                raise HTTPException(status_code=400, detail="La reserva ya se encuentra cancelada.")
            r["estado"] = "Cancelada"
            return r
            
    raise HTTPException(status_code=404, detail="Reserva no encontrada.")
