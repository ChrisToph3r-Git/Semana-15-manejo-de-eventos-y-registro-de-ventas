class Usuario:
    """Representa un usuario del restaurante."""

    def __init__(self, usuario, contrasena, nombre, correo):
        self.usuario = usuario
        self.contrasena = contrasena
        self.nombre = nombre
        self.correo = correo

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El usuario no puede estar vacío.")
        self._usuario = str(valor).strip()

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
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not valor or not str(valor).strip() or "@" not in str(valor):
            raise ValueError("Ingrese un correo electrónico válido.")
        self._correo = str(valor).strip()

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["usuario"],
            datos["contrasena"],
            datos["nombre"],
            datos["correo"]
        )
