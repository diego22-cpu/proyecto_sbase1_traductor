from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QPushButton, QMessageBox
import sys
import re

class TraductorApp(QMainWindow):
    def __init__(self, ui_file):
        super().__init__()
        uic.loadUi(ui_file, self)

        # Diccionario de traducción
        self.tokens = {
            'a': "11", 'b': "12", 'c': "13", 'd': "14", 'e': "15", 'f': "16",
            'g': "17", 'h': "18", 'i': "19", 'j': "20", 'k': "21", 'l': "22",
            'm': "23", 'n': "24", 'o': "25", 'p': "26", 'q': "27", 'r': "28",
            's': "29", 't': "30", 'u': "31", 'v': "32", 'w': "33", 'x': "34",
            'y': "35", 'z': "36", 'espacio': ".", 'LUNES': "2231241529",
            'MARTES': "231128301529", 'MIERCOLES': "231915281325221529"
        }
        self.reverse_tokens = {v: k for k, v in self.tokens.items()}

        # Elementos UI
        self.text_entrada = self.findChild(QTextEdit, "text_entrada")
        self.text_salida = self.findChild(QTextEdit, "text_salida")
        self.btn_traducir = self.findChild(QPushButton, "btn_traducir")
        self.btn_limpiar = self.findChild(QPushButton, "btn_limpiar")
        self.btn_ayuda = self.findChild(QPushButton, "btn_ayuda")

        # Conectar botones
        for button_name in self.tokens.keys():
            button = self.findChild(QPushButton, button_name)
            if button:
                button.clicked.connect(lambda _, name=button_name: self.on_button_click(name))

        self.btn_traducir.clicked.connect(self.traducir_texto)
        self.btn_limpiar.clicked.connect(self.limpiar_campos)
        self.btn_ayuda.clicked.connect(self.mostrar_ayuda)

    def on_button_click(self, button_name):
        """Inserta el código numérico correspondiente en el campo de entrada."""
        if button_name in self.tokens:
            texto_insercion = self.tokens[button_name]
            self.text_entrada.insertPlainText("." if button_name == 'espacio' else texto_insercion)

    def analizar_lexico(self, entrada):
        """Validación de tokens desconocidos."""
        bloques = entrada.split(".")
        for bloque in bloques:
            if not bloque:
                continue
            if bloque in self.reverse_tokens:
                continue
            if len(bloque) % 2 != 0:
                QMessageBox.warning(self, "Error Léxico", f"'{bloque}' tiene una longitud impar.")
                return False
            for i in range(0, len(bloque), 2):
                codigo = bloque[i:i + 2]
                if codigo not in self.reverse_tokens:
                    QMessageBox.warning(self, "Error Léxico", f"Código '{codigo}' no reconocido.")
                    return False
        return True

    def analizar_sintactico(self, entrada):
        """Verifica errores de formato antes de traducir."""
        if ".." in entrada or entrada.startswith(".") or entrada.endswith("."):
            QMessageBox.warning(self, "Error Sintáctico", "Formato de espacios incorrecto.")
            return False
        return True

    def traducir_texto(self):
        """Ejecuta análisis y traducción."""
        entrada = self.text_entrada.toPlainText().strip()
        if not entrada:
            QMessageBox.warning(self, "Advertencia", "El campo de entrada está vacío.")
            return

        if not self.analizar_lexico(entrada) or not self.analizar_sintactico(entrada):
            return

        # Traducción mejorada
        bloques = entrada.split(".")
        resultado = ""

        for bloque in bloques:
            if not bloque:
                continue
            if bloque in self.reverse_tokens:
                resultado += self.reverse_tokens[bloque] + " "
            else:
                traducido = ""
                for i in range(0, len(bloque), 2):
                    codigo = bloque[i:i + 2]
                    letra = self.reverse_tokens.get(codigo)
                    if letra:
                        traducido += letra
                    else:
                        QMessageBox.warning(self, "Error en Código", f"'{codigo}' no es válido.")
                        return
                resultado += traducido + " "

        self.text_salida.setPlainText(resultado.strip())

    def limpiar_campos(self):
        """Limpia los campos sin afectar la interfaz."""
        self.text_entrada.clear()
        self.text_salida.clear()

    def mostrar_ayuda(self):
        """Muestra las instrucciones de uso y posibles errores en un cuadro de diálogo."""
        mensaje = (
            "📌 **Instrucciones de Uso**\n"
            "Este traductor convierte códigos numéricos en texto.\n\n"
            "🔹 **Para escribir una palabra:**\n"
            "   - Presiona las letras y palabras disponibles.\n"
            "   - Usa el botón 'espacio' para separar palabras (genera '.').\n"
            "   - Pulsa 'Traducir' para ver el resultado.\n\n"
            "🔹 **Posibles Errores Léxicos:**\n"
            "   ❌ Código inválido (ejemplo: '99' no está definido).\n"
            "   ❌ Caracteres desconocidos (solo números y puntos son válidos).\n"
            "   ❌ Longitud impar (cada letra debe estar representada por 2 dígitos).\n\n"
            "🔹 **Posibles Errores Sintácticos:**\n"
            "   ❌ Doble punto consecutivo ('..') no permitido.\n"
            "   ❌ Iniciar o terminar con punto ('.texto' o 'texto.').\n"
            "   ❌ Secuencias incorrectas de caracteres que no cumplen las reglas establecidas.\n\n"
            "💡 **Consejo:** Si obtienes un error, revisa tu entrada y asegúrate de que siga la estructura correcta."
        )

        QMessageBox.information(self, "Ayuda del Traductor", mensaje)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_file = "tu_interfaz.ui"  # Tu archivo UI
    ventana = TraductorApp(ui_file)
    ventana.show()
    sys.exit(app.exec_())