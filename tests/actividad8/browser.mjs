import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';

// A8_NODE_MODULES permite usar una instalación ya disponible de Playwright.
// En un equipo normal basta con npm install en la raíz del repositorio.
const require = process.env.A8_NODE_MODULES
  ? createRequire(path.join(process.env.A8_NODE_MODULES, 'package.json'))
  : createRequire(import.meta.url);
const { chromium } = require('playwright');
const playwrightVersion = require('playwright/package.json').version;
const [caseId, baseUrl] = process.argv.slice(2);
assert.ok(['S01', 'S02'].includes(caseId), 'Caso desconocido');
const evidenceDir = path.resolve(process.env.A8_EVIDENCE_DIR || 'docs/actividad8/evidencias');
await fs.mkdir(evidenceDir, { recursive: true });
// Usa Chromium completo en modo headless, disponible también con --no-shell.
const launchOptions = process.env.A8_CHROMIUM_EXECUTABLE
  ? { headless: true, executablePath: process.env.A8_CHROMIUM_EXECUTABLE,
      args: JSON.parse(process.env.A8_CHROMIUM_ARGS || '[]') }
  : { headless: true, channel: 'chromium' };
const browser = await chromium.launch(launchOptions);
try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 1000 } });
  await page.goto(baseUrl);
  if (caseId === 'S01') {
    await page.screenshot({ path: path.join(evidenceDir, 'formulario-inicial.png'), fullPage: true });
  }
  const data = {
    nombre: 'Estudiante Prueba',
    correo: caseId === 'S01' ? 'estudiante@example.com' : 'correo-invalido',
    asunto: 'Consulta académica',
    mensaje: 'Solicito información del programa.',
  };
  for (const [key, value] of Object.entries(data)) await page.locator(`#${key}`).fill(value);
  const responsePromise = page.waitForResponse(r => r.request().method() === 'POST');
  await page.getByRole('button', { name: 'Enviar formulario' }).click();
  const response = await responsePromise;
  await page.waitForLoadState('load');
  const observed = {
    navegador: browser.version(), playwright: playwrightVersion,
    http_status: response.status(),
  };
  if (caseId === 'S01') {
    assert.equal(response.status(), 200);
    observed.confirmacion = await page.getByRole('status').innerText();
    assert.equal(observed.confirmacion, 'Formulario procesado correctamente. La información fue almacenada.');
    observed.campos_vacios = true;
    for (const key of Object.keys(data)) assert.equal(await page.locator(`#${key}`).inputValue(), '');
  } else {
    assert.equal(response.status(), 400);
    observed.error = await page.locator('#error-correo').innerText();
    assert.equal(observed.error, 'Ingrese un correo electrónico válido.');
    observed.aria_invalid = await page.locator('#correo').getAttribute('aria-invalid');
    observed.aria_describedby = await page.locator('#correo').getAttribute('aria-describedby');
    assert.equal(observed.aria_invalid, 'true');
    assert.equal(observed.aria_describedby, 'error-correo');
    observed.valores_conservados = {};
    for (const [key, value] of Object.entries(data)) {
      observed.valores_conservados[key] = await page.locator(`#${key}`).inputValue();
      assert.equal(observed.valores_conservados[key], value);
    }
    assert.equal(await page.getByRole('status').count(), 0);
  }
  await page.screenshot({ path: path.join(evidenceDir, `${caseId}.png`), fullPage: true });
  await fs.writeFile(path.join(evidenceDir, `${caseId}.html`), await page.content());
  console.log(JSON.stringify(observed));
} finally {
  await browser.close();
}
