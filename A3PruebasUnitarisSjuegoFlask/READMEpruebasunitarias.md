# Pruebas unitarias – Sistema de videojuegos (Flask + API REST)
    U3 - A3 Pruebas Unitarias en el Mini‑Proyecto Flask
    esarrollo de Bases de Datos para Web 129430 - Adolfo Castillo Chavarín 26B
    Jose Carlos Castro Arechiga


Pruebas unitarias con el módulo `unittest` de Python para la microaplicación de videojuegos. Cubren los modelos, las rutas protegidas y no protegidas, y la API RESTful.

## Estructura

...
tests/
├── test_models.py   # modelos Juego y User
├── test_routes.py   # rutas web, login, logout y registro
└── test_api.py      # API REST en /api/juegos
results.txt          # salida completa de la ejecución
README.md
...

## Cobertura

| Archivo | Pruebas | Qué verifica |
|---|---|---|
| `test_models.py` | 6 | Crear, guardar campos, actualizar y eliminar `Juego`; el password se guarda como hash; `username` es único. |
| `test_routes.py` | 7 | `/` redirige a `/juegos`; `/juegos` exige login; login incorrecto y correcto; logout; registro de usuario; ruta inexistente da 404. |
| `test_api.py` | 12 | GET lista y por id (200); POST crea (201); PUT actualiza (200); DELETE elimina (204); errores 400 (campos faltantes, precio inválido, cuerpo que no es JSON) y 404 (recurso inexistente). |

**Total: 25 pruebas.**

## Configuración de pruebas

La función `create_app('testing')` en `app.py` crea la aplicación con:

- Base de datos **SQLite en memoria** (`sqlite:///:memory:`), para no tocar la base MySQL real.
- `WTF_CSRF_ENABLED = False`, para poder enviar formularios desde las pruebas.

Cada clase de prueba usa `setUp` para crear la aplicación, el contexto y las tablas, y `tearDown` para borrar las tablas y cerrar el contexto. Así cada prueba empieza desde cero.

## Cómo ejecutar

Desde la raíz del proyecto, con el entorno virtual activado:

```powershell
python -m unittest discover -v tests
```

Para guardar la salida completa en `results.txt`:

```powershell
python -m unittest discover -v tests 2>&1 | Out-File -Encoding utf8 results.txt
```

Resultado esperado al final del archivo:

```
Ran 25 tests in 1.4xxs

OK
```

## Retos encontrados y soluciones

- **La carpeta se llamaba `test` y el comando busca `tests`.** Solución: renombrar la carpeta a `tests` y verificar que contenga los tres archivos `test_*.py`.
- **`ModuleNotFoundError: No module named 'flask_sqlalchemy'`.** Las dependencias no estaban instaladas en el Python que ejecutaba las pruebas. Solución: crear un entorno virtual (`venv`) e instalar `flask`, `flask-sqlalchemy`, `flask-login`, `flask-wtf`, `flask-restful` y `pymysql` dentro de él.
- **Las pruebas no debían usar MySQL.** Si usaran la base real, `tearDown` borraría las tablas con sus datos. Solución: la fábrica `create_app('testing')` con SQLite en memoria.
- **Los formularios tienen token CSRF y las pruebas no lo envían.** Solución: desactivar `WTF_CSRF_ENABLED` solo en la configuración de pruebas.
- **Un login incorrecto no redirige.** La aplicación vuelve a mostrar el formulario con código 200 y el mensaje de error. Solución: la prueba espera 200 y verifica el texto "incorrectos".
- **Aparecen avisos `ResourceWarning` en la salida.** Son advertencias de que algunas conexiones de SQLite en memoria no se cerraron explícitamente. No provocan fallos y todas las pruebas pasan. Quedan como mejora pendiente.
- **Al ejecutar desde PowerShell aparece texto rojo `NativeCommandError`.** Es el formato con el que PowerShell muestra lo que Python escribe en la salida de error. El resultado real está en `results.txt`.

## Notas

- El enunciado pide "MySQL en memoria". MySQL no ofrece una base en memoria como SQLite, por eso se usó SQLite en memoria para las pruebas. La aplicación normal sigue usando MySQL.
