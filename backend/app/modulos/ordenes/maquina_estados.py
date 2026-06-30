"""Maquina de estados que gobierna las transiciones de una orden."""
from __future__ import annotations

ESTADO_INICIAL = "PENDIENTE"

# Transiciones permitidas: estado actual -> estados a los que puede pasar.
TRANSICIONES_VALIDAS: dict[str, list[str]] = {
    "PENDIENTE": ["CONFIRMADO", "CANCELADO"],
    "CONFIRMADO": ["EN_PREPARACION", "CANCELADO"],
    "EN_PREPARACION": ["ENTREGADO", "CANCELADO"],
    "ENTREGADO": [],
    "CANCELADO": [],
}


def validar_transicion(estado_actual: str, estado_nuevo: str) -> bool:
    """Indica si pasar de ``estado_actual`` a ``estado_nuevo`` es legal."""
    return estado_nuevo in TRANSICIONES_VALIDAS.get(estado_actual, [])


def es_estado_terminal(estado: str) -> bool:
    """Indica si el estado no admite mas transiciones."""
    return not TRANSICIONES_VALIDAS.get(estado, ["placeholder"])


def estados_posibles(estado_actual: str) -> list[str]:
    """Lista los estados alcanzables desde el estado dado."""
    return list(TRANSICIONES_VALIDAS.get(estado_actual, []))
