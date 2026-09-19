"""
Backend - Gestión de Estudiantes y Sanciones
Proyecto: Proyecto-de-Biblioteca

Contiene toda la lógica de negocio del módulo.
El frontend debe comunicarse con este archivo y no manejar
directamente la estructura interna de los datos.
"""

from datetime import datetime


class Sanction:
    def __init__(self, reason, date=None, status="Activa"):
        self.reason = reason
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.status = status

    def __str__(self):
        return (
            f"Sanción: {self.reason} | "
            f"Fecha: {self.date} | Estado: {self.status}"
        )


class Student:
    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.sanctions = []

    def add_sanction(self, reason, date=None, status="Activa"):
        sanction = Sanction(reason, date, status)
        self.sanctions.append(sanction)
        return sanction

    def __str__(self):
        return (
            f"ID: {self.student_id} | "
            f"Nombre: {self.name} | "
            f"Correo: {self.email} | "
            f"Sanciones: {len(self.sanctions)}"
        )


class StudentManager:
    """Lógica de gestión de estudiantes y sanciones."""

    def __init__(self):
        self.students = {}

    # ---------- ESTUDIANTES ----------

    def add_student(self, student_id, name, email):
        if student_id in self.students:
            raise ValueError("Ya existe un estudiante con ese ID.")

        if not name.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if not email.strip():
            raise ValueError("El correo no puede estar vacío.")

        student = Student(student_id, name.strip(), email.strip())
        self.students[student_id] = student
        return student

    def get_student(self, student_id):
        return self.students.get(student_id)

    def find_student(self, student_id):
        return self.get_student(student_id)

    def list_students(self):
        return list(self.students.values())

    def search_students(self, text):
        text = str(text).strip().lower()

        return [
            student
            for student in self.students.values()
            if text in str(student.student_id).lower()
            or text in student.name.lower()
            or text in student.email.lower()
        ]

    def update_student(self, student_id, name=None, email=None):
        student = self.get_student(student_id)

        if student is None:
            return None

        if name is not None:
            if not name.strip():
                raise ValueError("El nombre no puede estar vacío.")
            student.name = name.strip()

        if email is not None:
            if not email.strip():
                raise ValueError("El correo no puede estar vacío.")
            student.email = email.strip()

        return student

    def remove_student(self, student_id):
        return self.students.pop(student_id, None)

    # ---------- SANCIONES ----------

    def add_sanction(self, student_id, reason, date=None, status="Activa"):
        student = self.get_student(student_id)

        if student is None:
            raise ValueError("El estudiante no existe.")

        if not reason.strip():
            raise ValueError("El motivo no puede estar vacío.")

        return student.add_sanction(reason.strip(), date, status)

    def get_sanctions(self, student_id):
        student = self.get_student(student_id)

        if student is None:
            return None

        return student.sanctions

    def remove_sanction(self, student_id, sanction_index):
        student = self.get_student(student_id)

        if student is None:
            return None

        if 0 <= sanction_index < len(student.sanctions):
            return student.sanctions.pop(sanction_index)

        return None

    def clear_sanctions(self, student_id):
        student = self.get_student(student_id)

        if student is None:
            return False

        student.sanctions.clear()
        return True

    # ---------- RESUMEN ----------

    def count_students(self):
        return len(self.students)

    def count_sanctions(self):
        return sum(len(s.sanctions) for s in self.students.values())

    def get_students_with_sanctions(self):
        return [
            student for student in self.students.values()
            if student.sanctions
        ]
