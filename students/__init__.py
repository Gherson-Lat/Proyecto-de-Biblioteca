"""Módulo de gestión de estudiantes y sanciones."""

from .backend import Student, Sanction, StudentManager
from .frontend import StudentFrontend

__all__ = [
    "Student",
    "Sanction",
    "StudentManager",
    "StudentFrontend",
]
