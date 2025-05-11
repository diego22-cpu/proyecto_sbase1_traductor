from PyQt5.QtWidgets import QApplication


class Conexion:
    @staticmethod
    def iniciar_aplicacion():
        """Inicializa la aplicación de PyQt5."""
        import sys  # Importamos aquí para modularizar mejor
        app = QApplication(sys.argv)
        return app
