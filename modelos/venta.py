class Venta:
    """Representa una venta realizada entre un usuario y un producto."""

    def __init__(self, usuario, producto, fecha):
        if not str(usuario).strip():
            raise ValueError("El usuario de la venta es obligatorio.")
        if not str(producto).strip():
            raise ValueError("El producto de la venta es obligatorio.")
        if not str(fecha).strip():
            raise ValueError("La fecha de la venta es obligatoria.")

        self.usuario = str(usuario).strip()
        self.producto = str(producto).strip()
        self.fecha = str(fecha).strip()

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(datos["usuario"], datos["producto"], datos["fecha"])

    def a_diccionario(self):
        return {
            "usuario": self.usuario,
            "producto": self.producto,
            "fecha": self.fecha
        }
