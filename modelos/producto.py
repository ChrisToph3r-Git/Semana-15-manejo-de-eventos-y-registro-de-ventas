class Producto:
    """Representa un producto del restaurante."""

    def __init__(self, codigo, nombre, categoria, precio, stock=0):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self._codigo = str(valor).strip()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = str(valor).strip()

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("La categoría no puede estar vacía.")
        self._categoria = str(valor).strip()

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        try:
            precio = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un número.")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        self._precio = precio

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        try:
            stock = int(valor)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un número entero.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = stock

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["codigo"],
            datos["nombre"],
            datos["categoria"],
            datos["precio"],
            datos.get("stock", 0)
        )

    def a_diccionario(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock
        }
