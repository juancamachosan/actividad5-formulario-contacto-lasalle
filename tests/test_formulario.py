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


def test_normaliza_espacios_laterales():
    ok, errors, data = process_form({
        "nombre": "  Juan Camacho  ",
        "correo": "  juan@example.com  ",
        "asunto": "  Consulta académica  ",
        "mensaje": "  Mensaje con espacios laterales.  "
    }, "testing")
    assert ok is True
    assert errors == {}
    assert data["nombre"] == "Juan Camacho"
    assert data["correo"] == "juan@example.com"
    assert data["asunto"] == "Consulta académica"
    assert data["mensaje"] == "Mensaje con espacios laterales."


def test_rechaza_campo_compuesto_solo_por_espacios():
    ok, errors, data = process_form({
        "nombre": "   ",
        "correo": "estudiante@lasalle.edu.co",
        "asunto": "Solicitud académica",
        "mensaje": "Mensaje válido."
    }, "testing")
    assert ok is False
    assert "nombre" in errors
    assert data["nombre"] == ""


def test_rechaza_nombre_que_supera_longitud_maxima():
    ok, errors, data = process_form({
        "nombre": "A" * 101,
        "correo": "estudiante@lasalle.edu.co",
        "asunto": "Solicitud académica",
        "mensaje": "Mensaje válido."
    }, "testing")
    assert ok is False
    assert "nombre" in errors
    assert "100" in errors["nombre"]


def test_rechaza_mensaje_que_supera_longitud_maxima():
    ok, errors, data = process_form({
        "nombre": "Estudiante Prueba",
        "correo": "estudiante@lasalle.edu.co",
        "asunto": "Solicitud académica",
        "mensaje": "M" * 2001
    }, "testing")
    assert ok is False
    assert "mensaje" in errors
    assert "2000" in errors["mensaje"]


def test_ambientes_usan_configuraciones_independientes():
    development = get_config("development")
    testing = get_config("testing")
    production = get_config("production")

    assert len({development.db_path, testing.db_path, production.db_path}) == 3
    assert development.debug is True
    assert testing.debug is True
    assert production.debug is False
