from pathlib import Path
import tkinter as tk
from tkinter import ttk


class LoginView:
    """Pantalla de acceso de la aplicación."""

    def __init__(self, root, restaurante_servicio, mostrar_principal):
        self.root = root
        self.restaurante_servicio = restaurante_servicio
        self.mostrar_principal = mostrar_principal
        self.contenedor = ttk.Frame(root, padding=40)
        self.contenedor.pack(fill="both", expand=True)

        self._configurar_estilo()
        self._crear_interfaz()

    def _configurar_estilo(self):
        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except ttk.TclError:
            pass
        estilo.configure("Titulo.TLabel", font=("Arial", 20, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Arial", 11))
        estilo.configure("Accion.TButton", padding=(12, 8))

    def _crear_interfaz(self):
        tarjeta = ttk.LabelFrame(
            self.contenedor,
            text="Inicio de sesión",
            padding=25
        )
        tarjeta.pack(expand=True)

        ruta_logo = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
        try:
            self.logo = tk.PhotoImage(file=str(ruta_logo))
            ttk.Label(tarjeta, image=self.logo).grid(
                row=0, column=0, columnspan=2, pady=(0, 15)
            )
        except Exception:
            ttk.Label(
                tarjeta, text="RESTAURANTE APP", style="Titulo.TLabel"
            ).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        ttk.Label(
            tarjeta, text="Acceso al sistema", style="Subtitulo.TLabel"
        ).grid(row=1, column=0, columnspan=2, pady=(0, 18))

        ttk.Label(tarjeta, text="Usuario").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.usuario_entry = ttk.Entry(tarjeta, width=32)
        self.usuario_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(tarjeta, text="Contraseña").grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )
        self.contrasena_entry = ttk.Entry(tarjeta, width=32, show="*")
        self.contrasena_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(
            tarjeta,
            text="Iniciar sesión",
            style="Accion.TButton",
            command=self.iniciar_sesion
        ).grid(row=4, column=0, columnspan=2, pady=15)

        self.mensaje = ttk.Label(tarjeta, text="")
        self.mensaje.grid(row=5, column=0, columnspan=2, pady=5)

        self.usuario_entry.focus()

    def iniciar_sesion(self):
        usuario = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()

        if not usuario or not contrasena:
            self.mensaje.config(text="Ingrese usuario y contraseña.")
            return

        usuario_validado = self.restaurante_servicio.validar_acceso(
            usuario, contrasena
        )

        if usuario_validado is None:
            self.mensaje.config(text="Usuario o contraseña incorrectos.")
            return

        self.mostrar_principal()
