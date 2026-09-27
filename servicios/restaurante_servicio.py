from datetime import datetime

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    """Contiene las operaciones, validaciones y reglas del restaurante."""

    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        self.usuarios = [
            Usuario.desde_diccionario(datos)
            for datos in self.archivo_servicio.cargar_usuarios()
        ]
        self.productos = [
            Producto.desde_diccionario(datos)
            for datos in self.archivo_servicio.cargar_productos()
        ]
        self.ventas = [
            Venta.desde_diccionario(datos)
            for datos in self.archivo_servicio.cargar_ventas()
        ]

    def validar_acceso(self, usuario, contrasena):
        for usuario_registrado in self.usuarios:
            if (
                usuario_registrado.usuario == usuario
                and usuario_registrado.contrasena == contrasena
            ):
                return usuario_registrado
        return None

    def listar_usuarios(self):
        return self.usuarios.copy()

    def listar_productos(self):
        return self.productos.copy()

    def listar_ventas(self):
        return self.ventas.copy()

    def obtener_usuario(self, nombre_usuario):
        nombre_usuario = str(nombre_usuario).strip()
        for usuario in self.usuarios:
            if usuario.usuario == nombre_usuario:
                return usuario
        return None

    def registrar_producto(self, codigo, nombre, categoria, precio, stock):
        if any(producto.codigo == str(codigo).strip() for producto in self.productos):
            raise ValueError("El código del producto ya existe.")

        producto = Producto(codigo, nombre, categoria, precio, stock)
        self.productos.append(producto)
        self._guardar_productos()
        return producto

    def obtener_producto(self, codigo):
        codigo = str(codigo).strip()
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto
        return None

    def actualizar_producto(self, codigo, nombre, categoria, precio, stock):
        producto = self.obtener_producto(codigo)
        if producto is None:
            raise ValueError("No se encontró un producto con ese código.")

        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        producto.stock = stock
        self._guardar_productos()
        return producto

    def eliminar_producto(self, codigo):
        producto = self.obtener_producto(codigo)
        if producto is None:
            raise ValueError("No se encontró un producto con ese código.")

        self.productos.remove(producto)
        self._guardar_productos()

    def registrar_venta(self, nombre_usuario, codigo_producto):
        usuario = self.obtener_usuario(nombre_usuario)
        if usuario is None:
            raise ValueError("El usuario seleccionado no existe.")

        producto = self.obtener_producto(codigo_producto)
        if producto is None:
            raise ValueError("El producto seleccionado no existe.")

        if producto.stock <= 0:
            raise ValueError("El producto seleccionado no tiene stock disponible.")

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        venta = Venta(usuario.usuario, producto.codigo, fecha)
        self.ventas.append(venta)
        self._guardar_ventas()
        return venta

    def _guardar_productos(self):
        self.archivo_servicio.guardar_productos(
            [producto.a_diccionario() for producto in self.productos]
        )

    def _guardar_ventas(self):
        self.archivo_servicio.guardar_ventas(
            [venta.a_diccionario() for venta in self.ventas]
        )
