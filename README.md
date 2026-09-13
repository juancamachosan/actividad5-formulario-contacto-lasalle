# Formulario de contacto La Salle

Aplicación web académica para demostrar la ejecución controlada de una misma solución en tres ambientes: desarrollo, pruebas y producción/demostración.

## Tecnologías

- Python 3.10 o superior
- Librería estándar de Python: `http.server`, `sqlite3`
- HTML5, CSS3
- SQLite como almacenamiento local independiente por ambiente

## Configuración

Copiar el archivo de ejemplo si se desea usar variables de entorno:

```bash
cp .env.example .env
```

No se incluyen contraseñas, tokens ni claves secretas.

## Ejecutar en ambiente de desarrollo

```bash
python app.py --env development --port 8000
```

Abrir: `http://127.0.0.1:8000`

Depuración habilitada, registros activos y base de datos `instance/contactos_development.db`.

## Ejecutar en ambiente de pruebas

```bash
python app.py --env testing --port 8001
```

Abrir: `http://127.0.0.1:8001`

Depuración habilitada para validar errores, datos identificables de prueba y base de datos `instance/contactos_testing.db`.

## Ejecutar pruebas automatizadas

```bash
python -m pytest -q
```

Casos cubiertos: envío correcto, campo obligatorio vacío y correo inválido.

## Ejecutar en producción/demostración local

```bash
python app.py --env production --host 0.0.0.0 --port 8002
```

Depuración deshabilitada y base de datos `instance/contactos_production.db`.

## Despliegue gratuito sugerido

Puede publicarse en Render, Railway, Replit o PythonAnywhere. Para Render, crear un Web Service, conectar el repositorio y usar:

```bash
python app.py --env production --host 0.0.0.0 --port $PORT
```

El archivo `Procfile` ya contiene el comando recomendado.
