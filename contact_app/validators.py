from __future__ import annotations
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
REQUIRED_FIELDS = {
    "nombre": "El nombre es obligatorio.",
    "correo": "El correo electrónico es obligatorio.",
    "asunto": "El asunto es obligatorio.",
    "mensaje": "El mensaje es obligatorio.",
}

def validate_contact(data: dict[str, str]) -> dict[str, str]:
    errors: dict[str, str] = {}
    for field, message in REQUIRED_FIELDS.items():
        if not data.get(field, "").strip():
            errors[field] = message
    if data.get("correo", "").strip() and not EMAIL_RE.match(data["correo"].strip()):
        errors["correo"] = "Ingrese un correo electrónico válido."
    return errors
