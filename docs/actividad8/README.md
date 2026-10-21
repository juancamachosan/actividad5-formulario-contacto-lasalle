# Actividad 8: pruebas del Formulario de contacto La Salle

Responsable: **Juan Andrés Camacho**. Equipo **1**, modalidad **individual**.

## Objeto y alcance

Se prueba el formulario funcional Python, HTML/CSS y SQLite del curso, que se conserva desde las actividades 4 y 5. La base de código es el commit `37bbf295f0321ae3ba17ca2b1bf9e261dc9e945d`. La actividad 6 añadió un prototipo estático con otros campos. Ese prototipo es un diseño separado, sin persistencia SQLite, y no forma parte de esta ejecución. No se utilizaron datos reales ni se enviaron mensajes a servicios de la Universidad.

Los identificadores RF01 a RF06 documentan reglas existentes, derivadas del código. Las pruebas unitarias aíslan el validador, las de integración conectan validación y persistencia real, y las de sistema recorren el formulario por navegador y HTTP.

## Resultados verificables

- Se diseñaron, automatizaron y ejecutaron **6 casos**: 2 unitarios, 2 de integración y 2 de sistema funcional.
- Resultado final de los seis: **6 aprobados**. Otras **8 pruebas previas** también pasaron.
- Salida total final: **14 passed in 3.31s**. [JUnit](evidencias/junit.xml), [salida sin editar](evidencias/pytest.txt) y [entorno](evidencias/entorno.json).
- [Diseño completo y resultados de cada caso](CASOS_DE_PRUEBA.md). [Datos estructurados](casos.json).
- [S01: envío correcto](evidencias/S01.png) y [S02: correo inválido](evidencias/S02.png). Las capturas provienen del navegador real y los JSON contienen resultados observados, sin datos personales reales.

El porcentaje aprobado corresponde a estos casos seleccionados. No mide cobertura total del código ni demuestra ausencia de defectos. No se ejecutaron pruebas de carga, seguridad integral, accesibilidad completa ni otros navegadores.

## Reproducción en Windows PowerShell

Requisitos: Python 3.10 o superior, Node.js 24 y Git. Ejecutar desde la raíz del repositorio:

```powershell
git switch test/actividad8
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tests/actividad8/requirements.txt
npm ci
npx playwright install chromium --no-shell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"
.\.venv\Scripts\python.exe -m pytest tests/actividad8 tests/test_formulario.py -vv --junitxml=docs/actividad8/evidencias/junit.xml
```

Para ejecutar solo los seis casos, omitir `tests/test_formulario.py` del último comando. En Linux o macOS cambiar el intérprete por `.venv/bin/python`. En Linux puede ser necesario `npx playwright install --with-deps chromium --no-shell`.

Los fixtures levantan y cierran el servidor automáticamente. Cada caso de integración o sistema utiliza una nueva ruta SQLite de `tmp_path`, sin acceder al almacenamiento de producción. El puerto lo asigna el sistema operativo. Las capturas y JSON se regeneran. Para conservar otro intento, usar la variable `A8_EVIDENCE_DIR` con una carpeta distinta antes de ejecutar. La suite previa usa únicamente el archivo local de testing de la copia de trabajo.

## Incidencia INC-01 y nueva ejecución

En el primer intento pasaron las 8 pruebas previas y 4 casos nuevos. S01 y S02 fallaron al iniciar Playwright por ausencia de `chromium_headless_shell-1234`. Un segundo intento con el canal Chromium también falló porque faltaba el binario completo. La descarga del navegador desde el CDN no produjo un archivo ZIP utilizable en este entorno.

La causa corresponde al entorno de automatización, antes de evaluar el comportamiento del formulario. La corrección aplicada consistió en instalar Chromium desde la distribución `@sparticuz/chromium` 153.0.0 y permitir en `browser.mjs` un ejecutable y argumentos explícitos mediante `A8_CHROMIUM_EXECUTABLE` y `A8_CHROMIUM_ARGS`. La aplicación no requirió cambios. El empaquetado necesitó extracción sin conservar propietarios de archivos en este contenedor.

La ejecución final usó Chromium 153.0.8010.0, Playwright 1.62.1, Node.js 24.19.0, Python 3.12.14 y pytest 8.4.2. El navegador alternativo se configuró solo en el entorno de ejecución. La ruta normal reproducible usa el canal Chromium instalado por Playwright. Se conservan [primer intento](evidencias/intento-inicial-pytest.txt), [JUnit inicial](evidencias/intento-inicial-junit.xml), [segundo intento](evidencias/segundo-intento-pytest.txt) y [resultado final](evidencias/pytest.txt).

En un entorno Linux con la misma distribución alternativa se puede instalar `@sparticuz/chromium@153.0.0` por separado y configurar dichas variables con su ejecutable y el JSON de `chromium.args`. `A8_NODE` y `A8_NODE_MODULES` permiten señalar instalaciones existentes de Node.js y Playwright. Su uso no cambia los pasos ni las aserciones de los seis casos.

## Hallazgos, acciones y conclusiones

No se detectaron defectos de la aplicación dentro de los seis escenarios ejecutados. INC-01 quedó resuelta y se verificó con una nueva ejecución completa. La validación del lado del servidor rechaza entradas inválidas y la comprobación de SQLite confirma la persistencia únicamente cuando corresponde.

Permanece una diferencia de alcance entre el prototipo visual de la Actividad 6 y el formulario funcional anterior. Se propone acordar una especificación única antes de integrar el rediseño. También se propone ampliar la matriz a otros navegadores, pruebas de seguridad y carga. Estas son acciones futuras, sin resultados de ejecución atribuidos.

El workflow del repositorio se amplió para instalar Node.js, Playwright y Chromium, ejecutar las 14 pruebas y conservar las evidencias como artefacto. El resultado local no equivale por sí solo a una ejecución aprobada en GitHub Actions.

## Contribución individual

| Responsable | Contribución | Entregable verificable |
|---|---|---|
|Juan Andrés Camacho|Definición de alcance, requisitos y estrategia|README y base RF01 a RF06|
|Juan Andrés Camacho|Diseño de los seis casos|CASOS_DE_PRUEBA.md y casos.json|
|Juan Andrés Camacho|Automatización, ejecución y análisis de incidencia|tests/actividad8 y evidencias|
|Juan Andrés Camacho|Organización de resultados y comunicación|Equipo_1_Actividad8.pptx y enlaces al repositorio|

## Referencias

1. ISTQB (2024). *Certified Tester Foundation Level Syllabus v4.0.1*, sección 2.2. https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
2. pytest. *How to invoke pytest*. https://docs.pytest.org/en/stable/how-to/usage.html
3. pytest. *Managing pytest's output: JUnitXML*. https://docs.pytest.org/en/stable/how-to/output.html
4. Microsoft. *Playwright: browsers*. https://playwright.dev/docs/browsers
5. Código fuente del Formulario de contacto La Salle, repositorio del curso. https://github.com/juancamachosan/actividad5-formulario-contacto-lasalle
6. Enunciado y rúbrica de la Actividad 8 aportados por el estudiante, octubre de 2026.

Consulta de documentación: 20 de octubre de 2026, America/Bogota.
