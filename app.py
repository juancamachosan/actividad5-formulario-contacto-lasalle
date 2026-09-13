#!/usr/bin/env python3
"""Formulario de contacto La Salle con tres ambientes controlados."""
from __future__ import annotations

import argparse
import html
import logging
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from contact_app.database import init_db, save_contact
from contact_app.settings import get_config
from contact_app.validators import MAX_LENGTHS, normalize_contact, validate_contact

ROOT = Path(__file__).resolve().parent


def process_form(
    form_data: dict[str, str], env: str | None = None
) -> tuple[bool, dict[str, str], dict[str, str]]:
    """Normaliza, valida y almacena un contacto.

    Retorna una tupla ``(ok, errors, clean_data)``. La base de datos solo se
    inicializa cuando la entrada supera todas las validaciones.
    """
    config = get_config(env)
    clean_data = normalize_contact(form_data)
    errors = validate_contact(clean_data)
    if errors:
        return False, errors, clean_data

    init_db(config.db_path)
    save_contact(config.db_path, clean_data, config.env)
    return True, {}, clean_data


def render_page(config, values=None, errors=None, success=False) -> str:
    values = values or {"nombre": "", "correo": "", "asunto": "", "mensaje": ""}
    errors = errors or {}

    debug_block = ""
    if config.debug:
        debug_block = (
            '<section class="debug-box" aria-label="Información de depuración">'
            '<strong>Modo depuración activo</strong><br>'
            f'Ambiente: {html.escape(config.env)}<br>'
            f'Almacenamiento: {html.escape(config.db_path)}<br>'
            f'Datos identificables: {html.escape(config.data_label)}'
            '</section>'
        )

    success_html = ""
    if success:
        success_html = (
            '<div class="alert success" role="status">'
            'Formulario procesado correctamente. La información fue almacenada.'
            '</div>'
        )

    def err(field: str) -> str:
        if not errors.get(field):
            return ""
        return (
            f'<small class="error" id="error-{field}" role="alert">'
            f'{html.escape(errors[field])}</small>'
        )

    def val(field: str) -> str:
        return html.escape(values.get(field, ""), quote=True)

    def aria(field: str) -> str:
        if errors.get(field):
            return f' aria-invalid="true" aria-describedby="error-{field}"'
        return ""

    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Formulario de contacto La Salle</title>
  <link rel="stylesheet" href="/static/styles.css">
</head>
<body class="env-{html.escape(config.env)}">
  <main class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Universidad de La Salle</p>
        <h1>Formulario de contacto La Salle</h1>
        <p>Aplicación web académica para demostrar ejecución controlada en desarrollo, pruebas y producción.</p>
      </div>
      <span class="badge">{html.escape(config.env.upper())}</span>
    </section>
    {debug_block}
    {success_html}
    <section class="card">
      <h2>Enviar mensaje</h2>
      <form method="post" action="/" novalidate>
        <label for="nombre">Nombre completo</label>
        <input id="nombre" type="text" name="nombre" value="{val('nombre')}" maxlength="{MAX_LENGTHS['nombre']}" autocomplete="name" required{aria('nombre')}>
        {err('nombre')}

        <label for="correo">Correo electrónico</label>
        <input id="correo" type="email" name="correo" value="{val('correo')}" maxlength="{MAX_LENGTHS['correo']}" autocomplete="email" required{aria('correo')}>
        {err('correo')}

        <label for="asunto">Asunto</label>
        <input id="asunto" type="text" name="asunto" value="{val('asunto')}" maxlength="{MAX_LENGTHS['asunto']}" autocomplete="off" required{aria('asunto')}>
        {err('asunto')}

        <label for="mensaje">Mensaje</label>
        <textarea id="mensaje" name="mensaje" rows="5" maxlength="{MAX_LENGTHS['mensaje']}" required{aria('mensaje')}>{html.escape(values.get('mensaje', ''))}</textarea>
        {err('mensaje')}

        <button type="submit">Enviar formulario</button>
      </form>
    </section>
  </main>
</body>
</html>'''


class ContactHandler(BaseHTTPRequestHandler):
    config = None

    def log_message(self, format, *args):
        if self.config and self.config.debug:
            super().log_message(format, *args)

    def _send_html(self, html_text: str, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(html_text.encode("utf-8"))

    def do_GET(self):
        if self.path == "/static/styles.css":
            css_path = ROOT / "static" / "styles.css"
            css = css_path.read_text(encoding="utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(css.encode("utf-8"))
            return

        if self.path != "/":
            self.send_error(404)
            return

        self._send_html(render_page(self.config))

    def do_POST(self):
        if self.path != "/":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            self.send_error(400, "Content-Length inválido")
            return

        body = self.rfile.read(length).decode("utf-8")
        raw = {key: values[0] for key, values in parse_qs(body, keep_blank_values=True).items()}
        ok, errors, clean = process_form(raw, self.config.env)

        if ok:
            logging.info("Contacto almacenado en ambiente %s", self.config.env)
            self._send_html(render_page(self.config, success=True))
        else:
            self._send_html(
                render_page(self.config, values=clean, errors=errors),
                status=400,
            )


def main():
    parser = argparse.ArgumentParser(description="Ejecuta Formulario de contacto La Salle")
    parser.add_argument(
        "--env",
        choices=["development", "testing", "production"],
        default=os.getenv("APP_ENV", "development"),
    )
    parser.add_argument("--host", default=os.getenv("APP_HOST", "127.0.0.1"))
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", os.getenv("APP_PORT", "8000"))),
    )
    args = parser.parse_args()

    config = get_config(args.env)
    level = logging.DEBUG if config.debug else logging.WARNING
    logging.basicConfig(level=level, format="[%(levelname)s] %(message)s")
    init_db(config.db_path)

    ContactHandler.config = config
    server = ThreadingHTTPServer((args.host, args.port), ContactHandler)
    print(
        f"Formulario La Salle ejecutándose en http://{args.host}:{args.port} "
        f"| ambiente={config.env} | debug={config.debug}"
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
