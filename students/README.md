# Gestión de Estudiantes y Sanciones

Módulo del Integrante 2 del proyecto de biblioteca.

## Estructura

- `backend.py`: lógica de estudiantes y sanciones.
- `frontend.py`: interfaz de consola.
- `test_students.py`: pruebas básicas.
- `__init__.py`: exporta las clases principales.

## Funciones

### Estudiantes
- Registrar
- Listar
- Buscar
- Actualizar
- Eliminar

### Sanciones
- Registrar
- Consultar
- Eliminar
- Consultar estudiantes sancionados

## Uso

Desde la carpeta `students`:

```bash
python frontend.py
```

Para probar el backend:

```bash
python test_students.py
```

Desde otro módulo del proyecto:

```python
from students.backend import StudentManager
```
