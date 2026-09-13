# Validación final

## Comando

`py -m pytest -q`

## Resultado local

`8 passed`

## Casos cubiertos

1. Envío válido y almacenamiento.
2. Campo obligatorio vacío.
3. Correo electrónico inválido.
4. Normalización de espacios laterales.
5. Campo compuesto únicamente por espacios.
6. Longitud máxima del nombre.
7. Longitud máxima del mensaje.
8. Separación de configuraciones por ambiente.

## Integración continua

El repositorio incluye `.github/workflows/tests.yml`, que ejecuta la misma suite automáticamente en `push` y `pull_request` sobre `main`.

## Seguridad

Se verificó que `.env`, bases SQLite y archivos generados localmente están excluidos del control de versiones mediante `.gitignore`.
