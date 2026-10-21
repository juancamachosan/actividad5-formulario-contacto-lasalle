# Actividad 8: casos de prueba completos

Juan Andrés Camacho. Equipo 1. Modalidad individual.

Objeto de prueba: formulario funcional Python/SQLite del repositorio del curso. El prototipo estático `actividad6/index.html` es un artefacto de diseño distinto y no sustituye el backend probado. No se evaluó el formulario público de la Universidad.

## Datos comunes D0

```json
{
  "nombre": "Estudiante Prueba",
  "correo": "estudiante@example.com",
  "asunto": "Consulta académica",
  "mensaje": "Solicito información del programa."
}
```

## Base de requisitos

Los identificadores se asignan en esta actividad para mantener la trazabilidad con el código existente. No constituyen requisitos nuevos de la institución.

| ID | Regla del alcance | Base verificable |
|---|---|---|
|RF01|Nombre, correo, asunto y mensaje obligatorios. Los espacios no satisfacen obligatoriedad.|validators.REQUIRED_FIELDS y validate_contact|
|RF02|Correo con formato básico conforme a EMAIL_RE del proyecto.|validators.EMAIL_RE|
|RF03|Mensaje de máximo 2000 caracteres.|validators.MAX_LENGTHS|
|RF04|Normalizar espacios y persistir solo entradas válidas en SQLite del ambiente.|app.process_form y database.save_contact|
|RF05|Envío válido: HTTP 200 y confirmación visible, con formulario limpio.|ContactHandler.do_POST y render_page|
|RF06|Envío inválido: HTTP 400, error asociado al campo, valores conservados y sin guardado.|ContactHandler.do_POST y render_page|

## Resumen

|ID|Nombre|Nivel|Estado final|
|---|---|---|---|
|U01|Nombre compuesto solo por espacios|Unitaria|Aprobado|
|U02|Límite del mensaje: 2000 y 2001 caracteres|Unitaria|Aprobado|
|I01|Persistencia del envío válido normalizado|Integración|Aprobado|
|I02|Correo inválido sin modificación de la base|Integración|Aprobado|
|S01|Envío válido desde el navegador|Sistema funcional|Aprobado|
|S02|Error de correo con conservación de datos|Sistema funcional|Aprobado|

## U01: Nombre compuesto solo por espacios

**Objetivo:** Rechazar un nombre sin caracteres útiles.

**Nivel:** Unitaria

**Requisito:** RF01. Obligatoriedad de los cuatro campos.

**Componente:** contact_app.validators.validate_contact

**Precondiciones:** Dependencias de Python instaladas. Validar la función en aislamiento, sin servidor ni base de datos.

**Datos de entrada:**

```json
{
  "nombre": "   ",
  "correo": "estudiante@example.com",
  "asunto": "Consulta académica",
  "mensaje": "Solicito información del programa."
}
```

**Pasos:**

1. Construir D0 y reemplazar nombre por tres espacios.
2. Invocar validate_contact(entrada).
3. Comparar el diccionario completo de errores.

**Resultado esperado:** Exactamente {"nombre": "El nombre es obligatorio."}.

**Resultado obtenido:** El validador devolvió exactamente el error de obligatoriedad del nombre.

**Estado final:** Aprobado

**Prueba automatizada:** `tests/actividad8/test_actividad8.py::test_U01_nombre_solo_espacios`.

**Evidencia:** [U01.json](evidencias/U01.json), [junit.xml](evidencias/junit.xml), [pytest.txt](evidencias/pytest.txt).

## U02: Límite del mensaje: 2000 y 2001 caracteres

**Objetivo:** Comprobar el límite superior y el primer valor fuera del límite.

**Nivel:** Unitaria

**Requisito:** RF03. El mensaje admite como máximo 2000 caracteres.

**Componente:** contact_app.validators.validate_contact

**Precondiciones:** Función en aislamiento. Los otros tres campos contienen los valores válidos de D0.

**Datos de entrada:**

```json
{
  "base": "D0",
  "mensaje_1": "M repetida 2000 veces",
  "mensaje_2": "M repetida 2001 veces"
}
```

**Pasos:**

1. Validar D0 con mensaje = "M" * 2000.
2. Validar D0 con mensaje = "M" * 2001.
3. Comparar ambos diccionarios de errores.

**Resultado esperado:** 2000: {}. 2001: {"mensaje": "El mensaje no puede superar 2000 caracteres."}.

**Resultado obtenido:** 2000 caracteres aceptados y 2001 rechazados con el error esperado.

**Estado final:** Aprobado

**Prueba automatizada:** `tests/actividad8/test_actividad8.py::test_U02_limite_mensaje_2000_2001`.

**Evidencia:** [U02.json](evidencias/U02.json), [junit.xml](evidencias/junit.xml), [pytest.txt](evidencias/pytest.txt).

## I01: Persistencia del envío válido normalizado

**Objetivo:** Verificar que normalización, validación y SQLite colaboran correctamente.

**Nivel:** Integración

**Requisito:** RF04. Un envío válido guarda una fila normalizada en el ambiente testing.

**Componente:** app.process_form + validators + database + SQLite real

**Precondiciones:** Fixture isolated_config: ruta SQLite nueva en tmp_path, sin contactos previos. Configuración testing temporal.

**Datos de entrada:**

```json
{
  "base": "D0",
  "transformacion": "Agregar dos espacios al principio y al final de cada campo."
}
```

**Pasos:**

1. Construir la entrada con espacios laterales.
2. Ejecutar process_form(entrada, "testing").
3. Consultar los cuatro campos y ambiente de todas las filas de SQLite.
4. Comparar el retorno y la fila completa con D0.

**Resultado esperado:** Retorno (True, {}, D0). Exactamente una fila, igual a D0 y ambiente = testing.

**Resultado obtenido:** Retorno correcto y una única fila normalizada, con los cuatro valores íntegros y ambiente testing.

**Estado final:** Aprobado

**Prueba automatizada:** `tests/actividad8/test_actividad8.py::test_I01_envio_valido_persistencia_normalizada`.

**Evidencia:** [I01.json](evidencias/I01.json), [junit.xml](evidencias/junit.xml), [pytest.txt](evidencias/pytest.txt).

## I02: Correo inválido sin modificación de la base

**Objetivo:** Evitar que una entrada rechazada se almacene o altere contactos existentes.

**Nivel:** Integración

**Requisito:** RF02. Formato de correo. RF04. Solo se guardan entradas válidas.

**Componente:** app.process_form + validators + SQLite real

**Precondiciones:** Base temporal de testing. Crear un contacto válido con D0 antes de ejecutar el intento inválido.

**Datos de entrada:**

```json
{
  "nombre": "Estudiante Prueba",
  "correo": "correo-invalido",
  "asunto": "Consulta académica",
  "mensaje": "Solicito información del programa."
}
```

**Pasos:**

1. Insertar D0 y guardar el conjunto de filas como antes.
2. Ejecutar process_form(entrada, "testing") con correo inválido.
3. Consultar de nuevo las filas como después.
4. Comparar retorno, error y conjuntos completos de filas.

**Resultado esperado:** ok=False y error de correo. Antes = después, con una fila y sin alteraciones.

**Resultado obtenido:** El correo produjo el error esperado. La fila previa permaneció idéntica y no se insertaron filas nuevas.

**Estado final:** Aprobado

**Prueba automatizada:** `tests/actividad8/test_actividad8.py::test_I02_correo_invalido_no_modifica_base`.

**Evidencia:** [I02.json](evidencias/I02.json), [junit.xml](evidencias/junit.xml), [pytest.txt](evidencias/pytest.txt).

## S01: Envío válido desde el navegador

**Objetivo:** Validar el recorrido completo de envío mediante la interfaz real.

**Nivel:** Sistema funcional

**Requisito:** RF04. Persistencia. RF05. Confirmación visible del envío válido.

**Componente:** Navegador + formulario HTML + HTTP POST + Python + SQLite

**Precondiciones:** Servidor real local en puerto libre, ambiente testing con SQLite temporal vacía. Playwright y Chromium instalados. Viewport 1280 × 1000.

**Datos de entrada:**

```json
{
  "nombre": "Estudiante Prueba",
  "correo": "estudiante@example.com",
  "asunto": "Consulta académica",
  "mensaje": "Solicito información del programa."
}
```

**Pasos:**

1. Abrir la URL del fixture live_server y completar los cuatro campos con D0.
2. Pulsar Enviar formulario y esperar la respuesta POST.
3. Verificar HTTP 200, texto de confirmación y campos vacíos.
4. Consultar SQLite y comparar la única fila con D0 más ambiente testing.

**Resultado esperado:** HTTP 200. Confirmación: Formulario procesado correctamente. La información fue almacenada. Campos vacíos y una fila exacta en SQLite.

**Resultado obtenido:** HTTP 200, confirmación exacta, cuatro campos vacíos y una fila con D0 en testing.

**Estado final:** Aprobado

**Prueba automatizada:** `tests/actividad8/test_actividad8.py::test_S01_envio_valido_desde_navegador`.

**Evidencia:** [S01.json](evidencias/S01.json), [junit.xml](evidencias/junit.xml), [pytest.txt](evidencias/pytest.txt), [S01.png](evidencias/S01.png), [S01.html](evidencias/S01.html).

## S02: Error de correo con conservación de datos

**Objetivo:** Comprobar que el usuario comprende el error y puede corregirlo sin volver a escribir todo.

**Nivel:** Sistema funcional

**Requisito:** RF02. Correo válido. RF06. Error visible, datos conservados y ausencia de guardado.

**Componente:** Navegador + formulario HTML + HTTP POST + Python + SQLite

**Precondiciones:** Servidor real local, ambiente testing con SQLite temporal vacía, Chromium y viewport 1280 × 1000.

**Datos de entrada:**

```json
{
  "nombre": "Estudiante Prueba",
  "correo": "correo-invalido",
  "asunto": "Consulta académica",
  "mensaje": "Solicito información del programa."
}
```

**Pasos:**

1. Abrir el formulario y completar la entrada indicada.
2. Pulsar Enviar formulario y esperar la respuesta POST.
3. Verificar HTTP 400 y el error Ingrese un correo electrónico válido.
4. Verificar aria-invalid=true y aria-describedby=error-correo.
5. Comparar los cuatro valores con la entrada. Confirmar ausencia de éxito y cero filas en SQLite.

**Resultado esperado:** HTTP 400, error junto al correo, atributos ARIA correctos, cuatro valores conservados, sin confirmación de éxito y cero filas.

**Resultado obtenido:** Todos los resultados esperados coincidieron. La base permaneció vacía.

**Estado final:** Aprobado

**Prueba automatizada:** `tests/actividad8/test_actividad8.py::test_S02_error_correo_conserva_datos`.

**Evidencia:** [S02.json](evidencias/S02.json), [junit.xml](evidencias/junit.xml), [pytest.txt](evidencias/pytest.txt), [S02.png](evidencias/S02.png), [S02.html](evidencias/S02.html).

