"""Envoltorio sobre el SDK de MercadoPago con degradacion controlada.

Si el SDK no esta instalado o no hay credenciales configuradas, las
funciones devuelven respuestas simuladas para permitir el desarrollo y las
pruebas locales sin conexion a la pasarela real.
"""
from __future__ import annotations

import uuid
from typing import Any

from app.nucleo.ajustes import ajustes


def _sdk_disponible() -> bool:
    if not ajustes.token_mp:
        return False
    try:
        import mercadopago  # noqa: F401
    except ImportError:
        return False
    return True


def crear_preferencia(items: list[dict[str, Any]], referencia: str) -> dict[str, Any]:
    """Crea una preferencia de pago y devuelve sus identificadores."""
    if not _sdk_disponible():
        identificador = f"sim-pref-{uuid.uuid4().hex[:12]}"
        return {
            "id": identificador,
            "init_point": f"https://simulado.local/checkout/{identificador}",
            "simulado": True,
        }

    import mercadopago

    cliente = mercadopago.SDK(ajustes.token_mp)

    _es_local = any(h in ajustes.url_frontend for h in ("localhost", "127.0.0.1"))

    cuerpo: dict[str, Any] = {
        "items": items,
        "external_reference": referencia,
    }
    if not _es_local:
        cuerpo["back_urls"] = {
            "success": f"{ajustes.url_frontend}/pago/exito",
            "failure": f"{ajustes.url_frontend}/pago/error",
            "pending": f"{ajustes.url_frontend}/pago/pendiente",
        }
        cuerpo["auto_return"] = "approved"
    if "localhost" not in ajustes.url_api and "127.0.0.1" not in ajustes.url_api:
        cuerpo["notification_url"] = f"{ajustes.url_api}/api/v1/cobros/webhook"
    respuesta = cliente.preference().create(cuerpo)
    datos = respuesta.get("response", {})
    return {
        "id": datos.get("id"),
        "init_point": datos.get("init_point"),
        "simulado": False,
    }


def consultar_pago(id_pago: str) -> dict[str, Any]:
    """Consulta el estado de un pago en MercadoPago."""
    if not _sdk_disponible():
        return {"id": id_pago, "status": "approved", "payment_method_id": "simulado"}

    import mercadopago

    cliente = mercadopago.SDK(ajustes.token_mp)
    respuesta = cliente.payment().get(id_pago)
    return respuesta.get("response", {})
