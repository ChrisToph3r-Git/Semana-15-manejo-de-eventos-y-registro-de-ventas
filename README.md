# restaurante_app - Semana 15

## Autor

Christopher Leonardo Paredes Jiménez

## Tema

Conceptos fundamentales de manejo de eventos en una aplicación orientada a objetos en Python.

## Descripción

Esta versión corresponde a la **Semana 15** y continúa el desarrollo de `restaurante_app` sobre la aplicación existente. El objetivo principal es aplicar los fundamentos básicos del manejo de eventos mediante una operación de **venta**.

La aplicación permite iniciar sesión, consultar usuarios, gestionar productos y registrar ventas. La nueva operación de ventas relaciona un usuario existente con un producto existente y utiliza un botón con `command=` para ejecutar un callback. El callback coordina la operación y delega las validaciones y el registro a `RestauranteServicio`.

## Objetivo de la Semana 15

Implementar una operación sencilla de venta que permita evidenciar el flujo de manejo de eventos:

```text
Acción del usuario
        ↓
Botón
        ↓
command=
        ↓
Callback
        ↓
RestauranteServicio
        ↓
Persistencia
        ↓
Actualización de la interfaz
        ↓
Respuesta visual
```

## Estructura del proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── logo.png
│   ├── menu.png
│   └── ventas.png
├── main.py
└── README.md
```

## Gestión de ventas

La Semana 15 incorpora una sección **Ventas** dentro de la aplicación. Esta sección permite:

1. Seleccionar un usuario existente mediante un `Combobox`.
2. Seleccionar un producto disponible mediante otro `Combobox`.
3. Presionar el botón **Registrar venta**.
4. Ejecutar el callback mediante `command=`.
5. Solicitar a `RestauranteServicio` la validación y el registro de la operación.
6. Crear una venta con usuario, producto y fecha.
7. Guardar la venta en `datos/ventas.json`.
8. Actualizar el `Treeview` para mostrar inmediatamente el registro.
9. Mostrar un mensaje indicando el resultado de la operación.

## Modelo Venta

La clase `Venta` representa una operación realizada entre un usuario y un producto. Contiene los siguientes datos:

- `usuario`
- `producto`
- `fecha`

El modelo también permite convertir los registros entre objetos y diccionarios para facilitar su persistencia en formato JSON.

## Manejo de eventos

El botón de registro de venta se encuentra asociado al método mediante `command=`:

```python
command=self.registrar_venta
```

El método `registrar_venta()` funciona como callback. Obtiene las selecciones realizadas en la interfaz, verifica que se hayan seleccionado los datos necesarios y solicita a `RestauranteServicio` que realice la operación.

La interfaz no contiene la lógica de persistencia de la venta. El servicio se encarga de validar la existencia del usuario y del producto, crear el registro y solicitar a `ArchivoServicio` que lo guarde.

## Persistencia

Las ventas se almacenan en:

```text
datos/ventas.json
```

`ArchivoServicio` se encarga de la lectura y escritura de los archivos JSON, mientras que `RestauranteServicio` mantiene las reglas de negocio relacionadas con la operación.

Al iniciar la aplicación, las ventas existentes se cargan desde `ventas.json`, permitiendo que los registros permanezcan disponibles después de cerrar y volver a ejecutar el programa.

## Interfaz y recursos visuales

La interfaz de la Semana 15 incorpora la sección de ventas y utiliza la carpeta obligatoria `assets/` para los recursos visuales del sistema.

Se utilizan:

- `Tk` para la ventana principal.
- `Frame` y `LabelFrame` para organizar las áreas de la aplicación.
- `Label` para textos y títulos.
- `Entry` para los campos de entrada existentes.
- `Combobox` para seleccionar usuarios y productos en la venta.
- `Button` con `command=` para ejecutar acciones y callbacks.
- `Treeview` para mostrar información y ventas registradas.
- `Scrollbar` para facilitar la navegación de las tablas.
- `assets/logo.png` como logotipo del sistema.
- `assets/menu.png` y `assets/ventas.png` como recursos visuales de la interfaz.

La navegación permite acceder a las secciones disponibles del sistema y registrar una venta sin manipular directamente los archivos JSON desde la interfaz.

## Funciones del sistema

### Inicio de sesión

La aplicación dispone de un acceso local y simulado. La validación de las credenciales se realiza mediante `RestauranteServicio`.

### Usuarios

Permite consultar la información de los usuarios almacenados en `datos/usuarios.json`.

### Productos

Mantiene las operaciones de gestión de productos disponibles en la aplicación:

- Registrar.
- Cargar / consultar.
- Actualizar.
- Eliminar.

### Ventas

Permite relacionar un usuario con un producto y registrar la operación mediante el flujo de eventos trabajado en la Semana 15.

## Credenciales de demostración

- Usuario: `admin`
- Contraseña: `1234`

También puede utilizarse:

- Usuario: `cliente`
- Contraseña: `1234`

El acceso es local y simulado con fines académicos.

## Requisitos

- Python 3.x
- Tkinter

No se requieren dependencias externas.

## Ejecución

Desde la carpeta raíz del proyecto:

```bash
python main.py
```

En Windows también puede utilizarse:

```bash
py main.py
```

## Comprobación del funcionamiento

1. Ejecutar `main.py`.
2. Iniciar sesión con una de las credenciales de demostración.
3. Comprobar que la aplicación muestre la interfaz principal.
4. Consultar la información de usuarios.
5. Comprobar que los productos disponibles se puedan gestionar.
6. Abrir la sección **Ventas**.
7. Seleccionar un usuario existente.
8. Seleccionar un producto existente.
9. Presionar **Registrar venta**.
10. Verificar que se ejecute el callback asociado mediante `command=`.
11. Comprobar el mensaje de resultado.
12. Verificar que la nueva venta aparezca en el `Treeview`.
13. Revisar que el registro se haya guardado en `datos/ventas.json`.
14. Cerrar y volver a ejecutar la aplicación.
15. Abrir nuevamente la sección Ventas y comprobar que los registros almacenados se recuperen correctamente.

## Alcance de la Semana 15

La actividad se concentra en los fundamentos básicos del manejo de eventos mediante `command=` y callbacks, utilizando la venta como operación práctica.

El proyecto no incorpora eventos avanzados como `bind()`, doble clic, eventos específicos de teclado o mouse ni `TreeviewSelect`, debido a que no forman parte del alcance solicitado para esta semana. Tampoco se implementan facturación, carrito de compras, inventario avanzado o bases de datos.

## Repositorio

El proyecto debe entregarse mediante un **repositorio público de GitHub** que contenga el código fuente, los archivos JSON, la carpeta `assets/` y este `README.md` correspondiente a la Semana 15.
