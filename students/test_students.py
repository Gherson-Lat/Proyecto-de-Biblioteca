from backend import StudentManager


def run_tests():
    manager = StudentManager()

    manager.add_student("1", "Ana", "ana@email.com")
    manager.add_student("2", "Luis", "luis@email.com")

    assert manager.count_students() == 2

    manager.add_sanction("1", "Entrega tardía de libro")
    assert manager.count_sanctions() == 1
    assert len(manager.get_sanctions("1")) == 1

    manager.update_student("2", name="Luis Actualizado")
    assert manager.get_student("2").name == "Luis Actualizado"

    assert len(manager.search_students("Luis")) == 1

    manager.remove_sanction("1", 0)
    assert manager.count_sanctions() == 0

    manager.remove_student("2")
    assert manager.count_students() == 1

    print("Todas las pruebas de backend pasaron correctamente.")


if __name__ == "__main__":
    run_tests()
