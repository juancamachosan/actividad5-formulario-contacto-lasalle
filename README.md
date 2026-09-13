# Formulario de contacto La Salle - Actividad 5

Proyecto académico de Ingeniería de Software que toma como base el **Formulario de contacto La Salle** de la Actividad 4 y lo gestiona mediante un flujo verificable de Git y GitHub.

## Integrante

- **Juan Andrés Camacho**
- Modalidad: **individual**
- GitHub: `juancamachosan`

## Tecnologías

- Python 3.10 o superior
- Librería estándar: `http.server`, `sqlite3`
- HTML5 y CSS3
- SQLite por ambiente
- `pytest` para pruebas automatizadas
- Git y GitHub para control de versiones

## Estructura

```text
.
├── app.py
├── contact_app/
├── static/
├── tests/
├── instance/
├── .env.example
├── .gitignore
├── requirements.txt
├── Procfile
└── runtime.txt
```

## Instalación

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

En Windows PowerShell, activar con:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Configuración

`.env.example` contiene únicamente valores de ejemplo. No se deben versionar archivos `.env`, contraseñas, tokens, claves privadas ni bases de datos locales.

## Ejecución

Desarrollo:

```bash
python app.py --env development --port 8000
```

Pruebas:

```bash
python app.py --env testing --port 8001
```

Producción/demostración local:

```bash
python app.py --env production --host 0.0.0.0 --port 8002
```

## Pruebas automatizadas

```bash
python -m pytest -q
```

La versión base conserva los tres casos de la Actividad 4: envío correcto, campo obligatorio vacío y correo inválido. La ampliación de cobertura se integra en una rama específica de pruebas.

## Flujo de trabajo

Los cambios de esta actividad se gestionan mediante issues, ramas y pull requests. La evidencia del conflicto controlado y de la validación final se incorporará en `docs/` durante el flujo de integración.
