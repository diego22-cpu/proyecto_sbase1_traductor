from conexion import Conexion
from traductor import TraductorApp


def main():

    app = Conexion.iniciar_aplicacion()


    ui_file = "Traductor.ui"


    ventana = TraductorApp(ui_file)


    ventana.show()


    app.exec_()


if __name__ == "__main__":
    main()
