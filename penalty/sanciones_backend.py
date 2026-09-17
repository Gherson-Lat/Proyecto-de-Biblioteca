from datetime import datetime

class Sancion:
    """Modelo de datos para representar una sanción individual."""
    PUNTOS_POR_DIA = 5

    def __init__(self, usuario: str, libro: str, dias_retraso: int):
        self.usuario = usuario
        self.libro = libro
        self.dias_retraso = int(dias_retraso)
        self.puntos_descontados = self.dias_retraso * self.PUNTOS_POR_DIA
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M")

    def a_dict(self):
        return {
            "usuario": self.usuario,
            "libro": self.libro,
            "dias_retraso": self.dias_retraso,
            "puntos": self.puntos_descontados,
            "fecha": self.fecha_registro
        }

class GestorSanciones:
    """Controlador/Gestor del modelo de datos para el historial."""
    def __init__(self):
        self._historial = []

    def registrar_sancion(self, usuario: str, libro: str, dias_retraso: int) -> Sancion:
        nueva_sancion = Sancion(usuario, libro, dias_retraso)
        self._historial.append(nueva_sancion)
        return nueva_sancion

    def obtener_historial(self):
        return [s.a_dict() for s in self._historial]