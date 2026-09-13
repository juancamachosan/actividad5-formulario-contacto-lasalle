# Evidencia de conflicto de integración

## Pull request involucrado
PR #7 - `feature/accesibilidad-formulario` -> `main`

https://github.com/juancamachosan/actividad5-formulario-contacto-lasalle/pull/7

## Causa
Las ramas `feature/validacion-formulario` y `feature/accesibilidad-formulario` se crearon desde una misma base y modificaron el mismo bloque de `app.py`.

La rama de validación fue integrada primero. Al intentar actualizar la rama de accesibilidad con `main`, Git detectó un conflicto de contenido en `app.py`.

## Resolución
Se revisaron manualmente los marcadores del conflicto y se conservaron ambas mejoras:

- normalización y límites de longitud;
- etiquetas HTML asociadas a campos;
- atributos `autocomplete`;
- atributos ARIA para errores;
- mensajes accesibles de validación.

La resolución quedó registrada mediante el commit:

`fix: resolver conflicto entre validación y accesibilidad del formulario`

## Validación posterior
Después de resolver el conflicto se ejecutó la suite base:

`3 passed`

Posteriormente se amplió la cobertura automatizada a ocho pruebas antes de la integración final.
