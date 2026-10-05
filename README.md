# restaurante_app - Semana 16

## Propósito

La Semana 16 continúa la aplicación del restaurante desarrollada en semanas anteriores. Agrega el manejo de eventos aplicado a la gestión de usuarios y conserva la estructura, navegación, inicio de sesión, gestión de productos, ventas y persistencia JSON del proyecto.

## Gestión de usuarios

La sección Usuarios permite registrar, consultar, actualizar y eliminar usuarios. Solo una cuenta con rol **Administrador** puede abrir esta sección; los usuarios de tipo Empleado y Cliente no ven el acceso administrativo. Los roles disponibles son **Administrador**, **Empleado** y **Cliente**.

La tabla muestra identificador, nombre, usuario y rol. No muestra contraseñas. Al seleccionar una fila, `<<TreeviewSelect>>` se atiende mediante `bind()`; el callback obtiene el identificador, consulta el usuario a través de `RestauranteServicio` y carga sus datos en el formulario.

## Eventos y callbacks

- Los botones Registrar, Actualizar, Eliminar y Limpiar conservan `command=` para invocar sus métodos.
- El `Combobox` de rol usa `bind("<<ComboboxSelected>>", ...)` para responder a cambios de selección.
- `bind_all("<Return>", ...)` permite registrar mediante el mismo método `registrar_usuario()`.
- `bind_all("<Escape>", ...)` limpia el formulario y cancela la selección mediante `limpiar_usuario()`.
- Los callbacks coordinan la interfaz y delegan las validaciones y operaciones a `RestauranteServicio`.

## Persistencia

Los usuarios se cargan y guardan en `datos/usuarios.json` usando `ArchivoServicio`. Los roles de las cuentas existentes se conservan en ese mismo archivo, por lo que los cambios persisten al cerrar y volver a iniciar la aplicación. Productos y ventas continúan usando sus archivos JSON existentes.

## Ejecución

Desde la carpeta del proyecto, ejecute:

```bash
python main.py
```
