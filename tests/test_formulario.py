import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import process_form
from contact_app.database import count_contacts
from contact_app.settings import get_config


def setup_module(module):
    db = Path(get_config("testing").db_path)
    if db.exists():
        db.unlink()


def test_envio_correcto_del_formulario():
    ok, errors, data = process_form({
        "nombre": "Estudiante Prueba",
        "correo": "estudiante@lasalle.edu.co",
        "asunto": "Solicitud académica",
        "mensaje": "Mensaje de prueba para validar almacenamiento."
    }, "testing")
    assert ok is True
    assert errors == {}
    assert count_contacts(get_config("testing").db_path) >= 1


def test_campo_obligatorio_vacio():
    ok, errors, data = process_form({
        "nombre": "",
        "correo": "estudiante@lasalle.edu.co",
        "asunto": "Solicitud académica",
        "mensaje": "Mensaje válido."
    }, "testing")
    assert ok is False
    assert "nombre" in errors


def test_correo_invalido():
    ok, errors, data = process_form({
        "nombre": "Estudiante Prueba",
        "correo": "correo-invalido",
        "asunto": "Solicitud académica",
        "mensaje": "Mensaje válido."
    }, "testing")
    assert ok is False
    assert "correo" in errors
