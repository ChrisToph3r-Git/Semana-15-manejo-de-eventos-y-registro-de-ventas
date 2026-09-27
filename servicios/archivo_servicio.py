import json
from pathlib import Path


class ArchivoServicio:
    """Administra la lectura y escritura de archivos JSON."""

    def __init__(self, carpeta_datos):
        self.carpeta_datos = Path(carpeta_datos)
        self.ruta_productos = self.carpeta_datos / "productos.json"
        self.ruta_usuarios = self.carpeta_datos / "usuarios.json"
        self.ruta_ventas = self.carpeta_datos / "ventas.json"

    def cargar_productos(self):
        return self._cargar_json(self.ruta_productos)

    def cargar_usuarios(self):
        return self._cargar_json(self.ruta_usuarios)

    def cargar_ventas(self):
        return self._cargar_json(self.ruta_ventas)

    def guardar_productos(self, productos):
        self._guardar_json(self.ruta_productos, productos)

    def guardar_ventas(self, ventas):
        self._guardar_json(self.ruta_ventas, ventas)

    def _cargar_json(self, ruta):
        try:
            with ruta.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        return datos if isinstance(datos, list) else []

    def _guardar_json(self, ruta, datos):
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
