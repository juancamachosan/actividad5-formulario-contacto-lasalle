from __future__ import annotations

import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

REQUIRED_FIELDS = {
    "nombre": "El nombre es obligatorio.",
    "correo": "El correo electrónico es obligatorio.",
    "asunto": "El asunto es obligatorio.",
    "mensaje": "El mensaje es obligatorio.",
}

MAX_LENGTHS = {
    "nombre": 100,
    "correo": 254,
    "asunto": 150,
    "mensaje": 2000,
}

FIELD_LABELS = {
    "nombre": "El nombre",
    "correo": "El correo electrónico",
    "asunto": "El asunto",
    "mensaje": "El mensaje",
}


def normalize_contact(data: dict[str, str]) -> dict[str, str]:
    """Retorna únicamente los campos permitidos, sin espacios laterales."""
    return {field: (data.get(field) or "").strip() for field in REQUIRED_FIELDS}


def validate_contact(data: dict[str, str]) -> dict[str, str]:
    """Valida obligatoriedad, longitud y formato de correo del contacto."""
    errors: dict[str, str] = {}

    for field, required_message in REQUIRED_FIELDS.items():
        value = data.get(field, "").strip()
        if not value:
            errors[field] = required_message
            continue

        max_length = MAX_LENGTHS[field]
        if len(value) > max_length:
            errors[field] = f"{FIELD_LABELS[field]} no puede superar {max_length} caracteres."

    email = data.get("correo", "").strip()
    if email and "correo" not in errors and not EMAIL_RE.fullmatch(email):
        errors["correo"] = "Ingrese un correo electrónico válido."

    return errors
