from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTANCE = ROOT / "instance"
INSTANCE.mkdir(exist_ok=True)

@dataclass(frozen=True)
class Config:
    env: str
    debug: bool
    db_path: str
    data_label: str

CONFIGS = {
    "development": Config("development", True, str(INSTANCE / "contactos_development.db"), "Datos de desarrollo: DEV-LASALLE-001"),
    "testing": Config("testing", True, str(INSTANCE / "contactos_testing.db"), "Datos de prueba: TEST-LASALLE-001"),
    "production": Config("production", False, str(INSTANCE / "contactos_production.db"), "Datos reales/demostración"),
}

def get_config(env: str | None = None) -> Config:
    selected = env or "development"
    if selected not in CONFIGS:
        raise ValueError(f"Ambiente no soportado: {selected}")
    return CONFIGS[selected]
