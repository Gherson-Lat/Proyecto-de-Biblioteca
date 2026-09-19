"""
Frontend - Gestión de Estudiantes y Sanciones

Interfaz de consola para utilizar el backend.
No contiene la lógica principal de datos; utiliza StudentManager.
"""

from backend import StudentManager


class StudentFrontend:
    def __init__(self, manager=None):
        self.manager = manager or StudentManager()

    def show_students(self):
        students = self.manager.list_students()

        print("\n=== ESTUDIANTES ===")

        if not students:
            print("No hay estudiantes registrados.")
            return

        for student in students:
            print(student)

    def register_student(self):
        try:
            student_id = input("ID del estudiante: ").strip()
            name = input("Nombre completo: ").strip()
            email = input("Correo electrónico: ").strip()

            student = self.manager.add_student(student_id, name, email)

            print("\nEstudiante registrado correctamente.")
            print(student)

        except ValueError as error:
            print(f"\nError: {error}")

    def search_student(self):
        text = input("Ingrese ID, nombre o correo: ").strip()
        results = self.manager.search_students(text)

        if not results:
            print("\nNo se encontraron estudiantes.")
            return

        print("\n=== RESULTADOS ===")
        for student in results:
            print(student)

    def update_student(self):
        student_id = input("ID del estudiante: ").strip()
        student = self.manager.get_student(student_id)

        if student is None:
            print("\nEl estudiante no existe.")
            return

        print("Deje vacío un campo si no desea modificarlo.")
        name = input(f"Nuevo nombre [{student.name}]: ").strip()
        email = input(f"Nuevo correo [{student.email}]: ").strip()

        try:
            self.manager.update_student(
                student_id,
                name=name if name else None,
                email=email if email else None
            )
            print("\nEstudiante actualizado correctamente.")

        except ValueError as error:
            print(f"\nError: {error}")

    def delete_student(self):
        student_id = input("ID del estudiante: ").strip()
        student = self.manager.remove_student(student_id)

        if student:
            print("\nEstudiante eliminado correctamente.")
        else:
            print("\nEl estudiante no existe.")

    def add_sanction(self):
        student_id = input("ID del estudiante: ").strip()
        reason = input("Motivo de la sanción: ").strip()

        try:
            sanction = self.manager.add_sanction(student_id, reason)
            print("\nSanción registrada correctamente.")
            print(sanction)

        except ValueError as error:
            print(f"\nError: {error}")

    def show_sanctions(self):
        student_id = input("ID del estudiante: ").strip()
        sanctions = self.manager.get_sanctions(student_id)

        if sanctions is None:
            print("\nEl estudiante no existe.")
            return

        print("\n=== SANCIONES ===")

        if not sanctions:
            print("El estudiante no tiene sanciones.")
            return

        for index, sanction in enumerate(sanctions, start=1):
            print(f"{index}. {sanction}")

    def remove_sanction(self):
        student_id = input("ID del estudiante: ").strip()
        sanctions = self.manager.get_sanctions(student_id)

        if sanctions is None:
            print("\nEl estudiante no existe.")
            return

        if not sanctions:
            print("\nEl estudiante no tiene sanciones.")
            return

        self.show_sanctions()
        try:
            number = int(input("Número de sanción a eliminar: "))
            removed = self.manager.remove_sanction(student_id, number - 1)

            if removed:
                print("\nSanción eliminada correctamente.")
            else:
                print("\nNúmero de sanción inválido.")

        except ValueError:
            print("\nDebe ingresar un número válido.")

    def menu(self):
        while True:
            print("""
=============================
 GESTIÓN DE ESTUDIANTES
=============================
1. Registrar estudiante
2. Listar estudiantes
3. Buscar estudiante
4. Actualizar estudiante
5. Eliminar estudiante
6. Registrar sanción
7. Ver sanciones
8. Eliminar sanción
0. Salir
""")

            option = input("Seleccione una opción: ").strip()

            if option == "1":
                self.register_student()
            elif option == "2":
                self.show_students()
            elif option == "3":
                self.search_student()
            elif option == "4":
                self.update_student()
            elif option == "5":
                self.delete_student()
            elif option == "6":
                self.add_sanction()
            elif option == "7":
                self.show_sanctions()
            elif option == "8":
                self.remove_sanction()
            elif option == "0":
                print("Programa finalizado.")
                break
            else:
                print("Opción inválida.")


if __name__ == "__main__":
    StudentFrontend().menu()
