# Guía de evidencias Git/GitHub - Actividad 5

Esta guía está diseñada para que el repositorio cumpla de forma verificable la rúbrica. No se deben crear commits vacíos ni cambios repetitivos para aumentar cantidades.

## 1. Crear el repositorio

Crear en GitHub un repositorio llamado:

```text
actividad5-formulario-contacto-lasalle
```

Puede ser público. Si es privado, agregar al docente como colaborador antes del cierre.

No inicializarlo con README, `.gitignore` o licencia si se va a subir primero la carpeta local preparada.

## 2. Configurar identidad propia

```bash
git config --global user.name "Juan Andrés Camacho"
git config --global user.email "CORREO_ASOCIADO_A_GITHUB"
```

Verificar:

```bash
git config user.name
git config user.email
```

## 3. Issue #1 - configuración y documentación

**Título**

```text
docs: preparar configuración y documentación reproducible
```

**Descripción**

```markdown
## Objetivo
Dejar el repositorio reproducible y seguro para la Actividad 5.

## Tareas
- [ ] Completar README con instalación, ejecución y pruebas.
- [ ] Fortalecer .gitignore para datos locales y secretos.
- [ ] Mantener .env.example sin datos sensibles.
- [ ] Agregar requirements.txt.
- [ ] Documentar estructura del proyecto.

## Criterio de aceptación
Una persona puede clonar el repositorio, instalar las dependencias y ejecutar aplicación y pruebas siguiendo únicamente el README.
```

**Rama**

```bash
git switch -c docs/configuracion-repositorio
```

Commits recomendados:

```text
docs: ampliar instalación, ejecución y estructura del proyecto
chore: proteger archivos locales y documentar configuración segura
```

Abrir PR:

```text
docs: preparar configuración y documentación reproducible
```

En el cuerpo incluir `Closes #1` y el resultado de `python -m pytest -q`.

## 4. Issue #2 - validación

**Título**

```text
feat: fortalecer validaciones del formulario
```

**Descripción**

```markdown
## Objetivo
Mejorar la validación sin alterar el propósito del formulario original.

## Tareas
- [ ] Centralizar normalización de datos.
- [ ] Rechazar entradas compuestas solo por espacios.
- [ ] Definir límites máximos de longitud.
- [ ] Aplicar maxlength en la interfaz.
- [ ] Mantener validación de correo.
```

**Rama**

```bash
git switch main
git pull
git switch -c feature/validacion-formulario
```

Commits recomendados:

```text
feat: centralizar normalización y límites de validación
feat: reflejar límites de validación en los campos HTML
```

Abrir PR y fusionarlo antes del Issue #3.

## 5. Issue #3 - accesibilidad y conflicto controlado

**Título**

```text
feat: mejorar accesibilidad y retroalimentación del formulario
```

La rama debe haberse creado desde el mismo punto anterior a la integración de `feature/validacion-formulario`, de modo que ambas modifiquen las mismas líneas en `app.py`.

**Cambios de esta rama**

- asociación `label`/`id`;
- `autocomplete`;
- `aria-invalid` y `aria-describedby`;
- `role="alert"` para errores;
- `role="status"` para confirmación.

Commits recomendados:

```text
feat: asociar etiquetas y campos para mejorar accesibilidad
feat: enlazar errores y confirmaciones con atributos aria
```

Al abrir el PR contra `main`, debe producirse el conflicto descrito en `CONFLICTO.md`. Resolver conservando **los límites de validación y los atributos de accesibilidad**.

Commit de resolución:

```text
fix: resolver conflicto entre validación y accesibilidad del formulario
```

Dejar un comentario en el PR:

```markdown
Conflicto resuelto de forma controlada en `app.py`. Se conservaron los `maxlength` de la rama de validación y los atributos `id`, `autocomplete`, `aria-invalid` y `aria-describedby` de la rama de accesibilidad. Después de la resolución se ejecutó nuevamente la suite de pruebas.
```

## 6. Issue #4 - pruebas y CI

**Título**

```text
test: ampliar pruebas y validar la versión integrada
```

**Rama**

```bash
git switch main
git pull
git switch -c test/pruebas-integracion
```

Tareas:

- ampliar `tests/test_formulario.py`;
- agregar `requirements.txt` si aún no se integró;
- agregar `.github/workflows/tests.yml`;
- ejecutar prueba final;
- actualizar `docs/VALIDACION_FINAL.md`.

Commits recomendados:

```text
test: ampliar cobertura de validaciones y ambientes
ci: ejecutar pytest automáticamente en push y pull request
docs: registrar validación final de la versión integrada
```

## 7. Verificación final del repositorio

Antes de entregar comprobar:

```bash
git log --oneline --graph --decorate --all
git branch -a
python -m pytest -q
git status
```

En GitHub deben quedar visibles:

- mínimo 4 issues;
- ramas utilizadas;
- mínimo 4 pull requests;
- commits significativos;
- PR/conflicto y su resolución;
- GitHub Actions aprobada;
- README y documentación;
- versión final en `main`.

## 8. Enlaces para el PDF

Guardar estos enlaces cuando existan:

```text
Repositorio: https://github.com/USUARIO/actividad5-formulario-contacto-lasalle
Issue #1: ...
Issue #2: ...
Issue #3: ...
Issue #4: ...
PR #1: ...
PR #2: ...
PR #3 (conflicto): ...
PR #4: ...
```

El PDF final no debe incluir enlaces ficticios; se genera únicamente cuando estas URLs existan.
