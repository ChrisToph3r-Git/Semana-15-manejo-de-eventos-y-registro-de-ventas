import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


class MainView:
    """Interfaz principal para usuarios, productos y ventas."""

    def __init__(self, root, restaurante_servicio, cerrar_sesion):
        self.root = root
        self.restaurante_servicio = restaurante_servicio
        self.cerrar_sesion = cerrar_sesion

        self.contenedor = ttk.Frame(root, padding=18)
        self.contenedor.pack(fill="both", expand=True)

        self._configurar_estilo()
        self._crear_encabezado()
        self._crear_navegacion()

        self.area_contenido = ttk.Frame(self.contenedor)
        self.area_contenido.pack(fill="both", expand=True, pady=(12, 0))

        self.mostrar_inicio()

    def _configurar_estilo(self):
        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("Titulo.TLabel", font=("Arial", 20, "bold"))
        estilo.configure("Seccion.TLabel", font=("Arial", 14, "bold"))
        estilo.configure("Accion.TButton", padding=(10, 6))
        estilo.configure("Treeview", rowheight=28)
        estilo.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    def _crear_encabezado(self):
        encabezado = ttk.Frame(self.contenedor)
        encabezado.pack(fill="x")

        ruta_logo = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
        try:
            self.logo = tk.PhotoImage(file=str(ruta_logo))
            ttk.Label(encabezado, image=self.logo).pack(side="left")
        except Exception:
            ttk.Label(
                encabezado, text="Restaurante App", style="Titulo.TLabel"
            ).pack(side="left")

        ttk.Button(
            encabezado,
            text="Cerrar sesión",
            style="Accion.TButton",
            command=self.cerrar_sesion
        ).pack(side="right")

    def _crear_navegacion(self):
        navegacion = ttk.LabelFrame(
            self.contenedor,
            text="Navegación",
            padding=8
        )
        navegacion.pack(fill="x", pady=12)

        ruta_menu = Path(__file__).resolve().parent.parent / "assets" / "menu.png"
        try:
            self.menu_icono = tk.PhotoImage(file=str(ruta_menu))
            ttk.Label(navegacion, image=self.menu_icono).pack(
                side="left", padx=(2, 8)
            )
        except Exception:
            pass

        for texto, comando in (
            ("Inicio", self.mostrar_inicio),
            ("Productos", self.mostrar_productos),
            ("Usuarios", self.mostrar_usuarios),
            ("Ventas", self.mostrar_ventas),
        ):
            boton = ttk.Button(
                navegacion,
                text=texto,
                style="Accion.TButton",
                command=comando
            )
            boton.pack(side="left", padx=4)

    def limpiar_contenido(self):
        for widget in self.area_contenido.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpiar_contenido()

        tarjeta = ttk.LabelFrame(
            self.area_contenido,
            text="Inicio",
            padding=25
        )
        tarjeta.pack(fill="both", expand=True)

        ttk.Label(
            tarjeta,
            text="Bienvenido al sistema del restaurante.",
            style="Seccion.TLabel"
        ).pack(pady=(35, 12))

        ttk.Label(
            tarjeta,
            text="Seleccione una sección para consultar información, "
                 "gestionar productos o registrar ventas."
        ).pack()

    def mostrar_productos(self):
        self.limpiar_contenido()

        formulario = ttk.LabelFrame(
            self.area_contenido,
            text="Datos del producto",
            padding=12
        )
        formulario.pack(fill="x", pady=(0, 10))

        self.codigo_entry = self._crear_campo(formulario, "Código", 0)
        self.nombre_entry = self._crear_campo(formulario, "Nombre", 1)
        self.categoria_entry = self._crear_campo(formulario, "Categoría", 2)
        self.precio_entry = self._crear_campo(formulario, "Precio", 3)
        self.stock_entry = self._crear_campo(formulario, "Stock", 4)

        acciones = ttk.Frame(formulario)
        acciones.grid(row=0, column=5, rowspan=5, padx=(18, 5), sticky="nsew")

        for texto, comando in (
            ("Registrar", self.registrar_producto),
            ("Cargar / Consultar", self.cargar_producto),
            ("Actualizar", self.actualizar_producto),
            ("Eliminar", self.eliminar_producto),
            ("Limpiar", self.limpiar_formulario),
        ):
            ttk.Button(
                acciones, text=texto, style="Accion.TButton", command=comando
            ).pack(fill="x", pady=3)

        tabla_frame = ttk.LabelFrame(
            self.area_contenido,
            text="Productos registrados",
            padding=8
        )
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tabla = ttk.Treeview(
            tabla_frame, columns=columnas, show="headings", height=9
        )
        encabezados = {
            "codigo": "Código", "nombre": "Nombre", "categoria": "Categoría",
            "precio": "Precio", "stock": "Stock"
        }

        for columna in columnas:
            self.tabla.heading(columna, text=encabezados[columna])

        self.tabla.column("codigo", width=75, anchor="center")
        self.tabla.column("nombre", width=170)
        self.tabla.column("categoria", width=150)
        self.tabla.column("precio", width=85, anchor="e")
        self.tabla.column("stock", width=70, anchor="center")

        scroll = ttk.Scrollbar(
            tabla_frame, orient="vertical", command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.actualizar_tabla()

    def _crear_campo(self, contenedor, texto, fila):
        ttk.Label(contenedor, text=texto).grid(
            row=fila, column=0, sticky="w", padx=5, pady=4
        )
        entry = ttk.Entry(contenedor, width=28)
        entry.grid(row=fila, column=1, padx=5, pady=4)
        return entry

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for producto in self.restaurante_servicio.listar_productos():
            self.tabla.insert(
                "", "end",
                values=(
                    producto.codigo, producto.nombre, producto.categoria,
                    f"${producto.precio:.2f}", producto.stock
                )
            )

    def registrar_producto(self):
        try:
            self.restaurante_servicio.registrar_producto(
                self.codigo_entry.get(), self.nombre_entry.get(),
                self.categoria_entry.get(), self.precio_entry.get(),
                self.stock_entry.get()
            )
            self.actualizar_tabla()
            self.limpiar_formulario()
            messagebox.showinfo("Producto", "Producto registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def cargar_producto(self):
        producto = self.restaurante_servicio.obtener_producto(
            self.codigo_entry.get()
        )
        if producto is None:
            messagebox.showerror(
                "Consulta", "No se encontró un producto con ese código."
            )
            return

        for entry, valor in (
            (self.nombre_entry, producto.nombre),
            (self.categoria_entry, producto.categoria),
            (self.precio_entry, producto.precio),
            (self.stock_entry, producto.stock),
        ):
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    def actualizar_producto(self):
        try:
            self.restaurante_servicio.actualizar_producto(
                self.codigo_entry.get(), self.nombre_entry.get(),
                self.categoria_entry.get(), self.precio_entry.get(),
                self.stock_entry.get()
            )
            self.actualizar_tabla()
            messagebox.showinfo("Producto", "Producto actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def eliminar_producto(self):
        codigo = self.codigo_entry.get().strip()
        if not codigo:
            messagebox.showerror("Error", "Ingrese el código del producto.")
            return

        if not messagebox.askyesno(
            "Eliminar producto",
            f"¿Desea eliminar el producto con código {codigo}?"
        ):
            return

        try:
            self.restaurante_servicio.eliminar_producto(codigo)
            self.actualizar_tabla()
            self.limpiar_formulario()
            messagebox.showinfo("Producto", "Producto eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def limpiar_formulario(self):
        for entry in (
            self.codigo_entry, self.nombre_entry, self.categoria_entry,
            self.precio_entry, self.stock_entry
        ):
            entry.delete(0, tk.END)

    def mostrar_usuarios(self):
        self.limpiar_contenido()

        contenedor = ttk.LabelFrame(
            self.area_contenido, text="Usuarios registrados", padding=12
        )
        contenedor.pack(fill="both", expand=True)

        columnas = ("usuario", "nombre", "correo")
        tabla = ttk.Treeview(
            contenedor, columns=columnas, show="headings"
        )
        for columna, titulo in (
            ("usuario", "Usuario"), ("nombre", "Nombre"), ("correo", "Correo")
        ):
            tabla.heading(columna, text=titulo)

        tabla.column("usuario", width=130)
        tabla.column("nombre", width=220)
        tabla.column("correo", width=250)

        for usuario in self.restaurante_servicio.listar_usuarios():
            tabla.insert(
                "", "end",
                values=(usuario.usuario, usuario.nombre, usuario.correo)
            )
        tabla.pack(fill="both", expand=True)

    def mostrar_ventas(self):
        self.limpiar_contenido()

        formulario = ttk.LabelFrame(
            self.area_contenido,
            text="Registrar venta",
            padding=14
        )
        formulario.pack(fill="x", pady=(0, 10))

        ttk.Label(formulario, text="Usuario").grid(
            row=0, column=0, padx=5, pady=6, sticky="w"
        )
        usuarios = [usuario.usuario for usuario in self.restaurante_servicio.listar_usuarios()]
        self.usuario_combo = ttk.Combobox(
            formulario, values=usuarios, state="readonly", width=28
        )
        self.usuario_combo.grid(row=0, column=1, padx=5, pady=6)

        ttk.Label(formulario, text="Producto").grid(
            row=1, column=0, padx=5, pady=6, sticky="w"
        )
        productos = [
            f"{producto.codigo} - {producto.nombre}"
            for producto in self.restaurante_servicio.listar_productos()
            if producto.stock > 0
        ]
        self.producto_combo = ttk.Combobox(
            formulario, values=productos, state="readonly", width=36
        )
        self.producto_combo.grid(row=1, column=1, padx=5, pady=6)

        ruta_icono = Path(__file__).resolve().parent.parent / "assets" / "ventas.png"
        try:
            self.ventas_icono = tk.PhotoImage(file=str(ruta_icono))
            ttk.Label(formulario, image=self.ventas_icono).grid(
                row=0, column=2, rowspan=2, padx=12
            )
        except Exception:
            pass

        ttk.Button(
            formulario,
            text="Registrar venta",
            style="Accion.TButton",
            command=self.registrar_venta
        ).grid(row=0, column=3, rowspan=2, padx=10, pady=6)

        tabla_frame = ttk.LabelFrame(
            self.area_contenido, text="Ventas registradas", padding=8
        )
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("usuario", "producto", "fecha")
        self.tabla_ventas = ttk.Treeview(
            tabla_frame, columns=columnas, show="headings", height=12
        )
        for columna, titulo in (
            ("usuario", "Usuario"),
            ("producto", "Producto"),
            ("fecha", "Fecha y hora"),
        ):
            self.tabla_ventas.heading(columna, text=titulo)

        self.tabla_ventas.column("usuario", width=180)
        self.tabla_ventas.column("producto", width=180)
        self.tabla_ventas.column("fecha", width=220)

        scroll = ttk.Scrollbar(
            tabla_frame, orient="vertical", command=self.tabla_ventas.yview
        )
        self.tabla_ventas.configure(yscrollcommand=scroll.set)
        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.actualizar_tabla_ventas()

    def registrar_venta(self):
        usuario = self.usuario_combo.get().strip()
        seleccion_producto = self.producto_combo.get().strip()

        if not usuario or not seleccion_producto:
            messagebox.showerror(
                "Venta", "Seleccione un usuario y un producto."
            )
            return

        codigo_producto = seleccion_producto.split(" - ", 1)[0]

        try:
            self.restaurante_servicio.registrar_venta(
                usuario, codigo_producto
            )
            self.actualizar_tabla_ventas()
            self.mostrar_ventas()
            messagebox.showinfo("Venta", "Venta registrada correctamente.")
        except ValueError as error:
            messagebox.showerror("Venta", str(error))

    def actualizar_tabla_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        productos = {
            producto.codigo: producto.nombre
            for producto in self.restaurante_servicio.listar_productos()
        }

        for venta in self.restaurante_servicio.listar_ventas():
            nombre_producto = productos.get(venta.producto, venta.producto)
            self.tabla_ventas.insert(
                "", "end",
                values=(venta.usuario, nombre_producto, venta.fecha)
            )
