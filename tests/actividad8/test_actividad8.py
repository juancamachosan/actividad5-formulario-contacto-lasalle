"""Seis casos de Actividad 8. Todos usan datos sintéticos y SQLite temporal."""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import sys
import threading
from dataclasses import replace
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app import ContactHandler, process_form
from contact_app.database import init_db
from contact_app.settings import CONFIGS
from contact_app.validators import validate_contact

BASE = {
    "nombre": "Estudiante Prueba",
    "correo": "estudiante@example.com",
    "asunto": "Consulta académica",
    "mensaje": "Solicito información del programa.",
}


def evidence(case_id, observed):
    destination = Path(os.getenv("A8_EVIDENCE_DIR", ROOT / "docs/actividad8/evidencias"))
    destination.mkdir(parents=True, exist_ok=True)
    result = {
        "caso": case_id,
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "observado": observed,
    }
    (destination / f"{case_id}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def rows(db_path):
    with sqlite3.connect(db_path) as connection:
        return connection.execute(
            "SELECT nombre, correo, asunto, mensaje, ambiente FROM contactos ORDER BY id"
        ).fetchall()


@pytest.fixture
def isolated_config(tmp_path, monkeypatch):
    config = replace(CONFIGS["testing"], db_path=str(tmp_path / "contactos_testing.db"))
    monkeypatch.setitem(CONFIGS, "testing", config)
    return config


@pytest.fixture
def live_server(isolated_config):
    init_db(isolated_config.db_path)
    handler = type("IsolatedContactHandler", (ContactHandler,), {"config": isolated_config})
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}", isolated_config
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_U01_nombre_solo_espacios():
    errors = validate_contact({**BASE, "nombre": "   "})
    evidence("U01", {"errores": errors})
    assert errors == {"nombre": "El nombre es obligatorio."}


def test_U02_limite_mensaje_2000_2001():
    accepted = validate_contact({**BASE, "mensaje": "M" * 2000})
    rejected = validate_contact({**BASE, "mensaje": "M" * 2001})
    evidence("U02", {"errores_2000": accepted, "errores_2001": rejected})
    assert accepted == {}
    assert rejected == {"mensaje": "El mensaje no puede superar 2000 caracteres."}


def test_I01_envio_valido_persistencia_normalizada(isolated_config):
    payload = {key: f"  {value}  " for key, value in BASE.items()}
    ok, errors, clean = process_form(payload, "testing")
    stored = rows(isolated_config.db_path)
    evidence("I01", {"ok": ok, "errores": errors, "datos_limpios": clean, "filas": stored})
    assert (ok, errors, clean) == (True, {}, BASE)
    assert stored == [tuple(BASE.values()) + ("testing",)]


def test_I02_correo_invalido_no_modifica_base(isolated_config):
    assert process_form(BASE, "testing")[0] is True
    before = rows(isolated_config.db_path)
    ok, errors, clean = process_form({**BASE, "correo": "correo-invalido"}, "testing")
    after = rows(isolated_config.db_path)
    evidence("I02", {"ok": ok, "errores": errors, "filas_antes": before, "filas_despues": after})
    assert ok is False
    assert errors == {"correo": "Ingrese un correo electrónico válido."}
    assert len(before) == 1
    assert after == before


def run_browser(case_id, live_server):
    url, config = live_server
    node = os.getenv("A8_NODE") or shutil.which("node")
    assert node, "Instale Node.js para ejecutar los dos casos funcionales."
    result = subprocess.run(
        [node, str(ROOT / "tests/actividad8/browser.mjs"), case_id, url],
        cwd=ROOT, capture_output=True, text=True, timeout=90,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    observed = json.loads(result.stdout)
    stored = rows(config.db_path)
    evidence(case_id, {**observed, "filas": stored})
    expected = [tuple(BASE.values()) + ("testing",)] if case_id == "S01" else []
    assert stored == expected


def test_S01_envio_valido_desde_navegador(live_server):
    run_browser("S01", live_server)


def test_S02_error_correo_conserva_datos(live_server):
    run_browser("S02", live_server)
