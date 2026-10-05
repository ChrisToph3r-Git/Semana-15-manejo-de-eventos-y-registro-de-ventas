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
        self.usuario_actual = None
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
                self.usuario_actual = usuario_registrado
                return usuario_registrado
        self.usuario_actual = None
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

    def registrar_usuario(self, usuario, contrasena, nombre, rol, identificacion=None):
        if self.obtener_usuario(usuario) is not None:
            raise ValueError("El nombre de usuario ya existe.")
        identificacion = identificacion if identificacion is not None else usuario
        if any(registrado.identificacion == str(identificacion).strip() for registrado in self.usuarios):
            raise ValueError("El ID / Identificación ya existe.")
        if rol == "Administrador":
            raise ValueError("La gestión administrativa permite registrar Empleados o Clientes.")
        nuevo_usuario = Usuario(usuario, contrasena, nombre, rol, identificacion)
        self.usuarios.append(nuevo_usuario)
        self._guardar_usuarios()
        return nuevo_usuario

    def actualizar_usuario(self, identificador, contrasena, nombre, rol, identificacion=None):
        usuario = self.obtener_usuario(identificador)
        if usuario is None:
            raise ValueError("No se encontró el usuario seleccionado.")
        if usuario.rol == "Administrador" or rol == "Administrador":
            raise ValueError("Solo se pueden actualizar usuarios Empleado o Cliente.")
        if identificacion is not None and any(
            registrado is not usuario
            and registrado.identificacion == str(identificacion).strip()
            for registrado in self.usuarios
        ):
            raise ValueError("El ID / Identificación ya existe.")
        usuario.contrasena = contrasena
        usuario.nombre = nombre
        usuario.rol = rol
        if identificacion is not None:
            usuario.identificacion = identificacion
        self._guardar_usuarios()
        return usuario

    def eliminar_usuario(self, identificador):
        usuario = self.obtener_usuario(identificador)
        if usuario is None:
            raise ValueError("No se encontró el usuario seleccionado.")
        if usuario.rol == "Administrador":
            raise ValueError("No se puede eliminar un usuario Administrador.")
        if self.usuario_actual is usuario:
            raise ValueError("No puede eliminar la cuenta que está utilizando.")
        self.usuarios.remove(usuario)
        self._guardar_usuarios()

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

    def _guardar_usuarios(self):
        self.archivo_servicio.guardar_usuarios(
            [usuario.a_diccionario() for usuario in self.usuarios]
        )

    def _guardar_ventas(self):
        self.archivo_servicio.guardar_ventas(
            [venta.a_diccionario() for venta in self.ventas]
        )
