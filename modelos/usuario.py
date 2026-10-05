class Usuario:
    """Representa un usuario del restaurante."""

    ROLES = ("Administrador", "Empleado", "Cliente")

    def __init__(self, usuario, contrasena, nombre, rol="Cliente", identificacion=None):
        self.identificacion = identificacion if identificacion is not None else usuario
        self.usuario = usuario
        self.contrasena = contrasena
        self.nombre = nombre
        self.rol = rol

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El usuario no puede estar vacío.")
        self._usuario = str(valor).strip()

    @property
    def identificacion(self):
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El ID / Identificación no puede estar vacío.")
        self._identificacion = str(valor).strip()

    @property
    def contrasena(self):
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("La contraseña no puede estar vacía.")
        self._contrasena = str(valor).strip()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = str(valor).strip()

    @property
    def rol(self):
        return self._rol

    @rol.setter
    def rol(self, valor):
        if valor not in self.ROLES:
            raise ValueError("Seleccione un rol válido.")
        self._rol = valor

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["usuario"],
            datos["contrasena"],
            datos["nombre"],
            datos.get("rol", "Cliente"),
            datos.get("identificacion", datos["usuario"])
        )

    def a_diccionario(self):
        return {
            "usuario": self.usuario,
            "identificacion": self.identificacion,
            "contrasena": self.contrasena,
            "nombre": self.nombre,
            "rol": self.rol,
        }
