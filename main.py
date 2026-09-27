import tkinter as tk
from pathlib import Path

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class AplicacionRestaurante:
    """Punto de entrada y coordinación de las vistas."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restaurante App - Semana 15")
        self.root.geometry("980x700")
        self.root.minsize(820, 620)

        ruta_base = Path(__file__).resolve().parent
        archivo_servicio = ArchivoServicio(ruta_base / "datos")
        self.restaurante_servicio = RestauranteServicio(archivo_servicio)

        self.vista_actual = None
        self.mostrar_login()

    def cambiar_vista(self, nueva_vista):
        if self.vista_actual is not None:
            self.vista_actual.contenedor.destroy()
        self.vista_actual = nueva_vista

    def mostrar_login(self):
        vista = LoginView(
            self.root,
            self.restaurante_servicio,
            self.mostrar_principal
        )
        self.cambiar_vista(vista)

    def mostrar_principal(self):
        vista = MainView(
            self.root,
            self.restaurante_servicio,
            self.mostrar_login
        )
        self.cambiar_vista(vista)

    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":
    AplicacionRestaurante().ejecutar()
