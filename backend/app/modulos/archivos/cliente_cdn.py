"""Envoltorio sobre el SDK de Cloudinary con degradacion controlada."""
from __future__ import annotations

import uuid
from typing import Any

from app.nucleo.ajustes import ajustes


def _cdn_disponible() -> bool:
    if not (ajustes.nube_cdn and ajustes.api_key_cdn and ajustes.api_secret_cdn):
        return False
    try:
        import cloudinary  # noqa: F401
    except ImportError:
        return False
    return True


def _configurar() -> None:
    import cloudinary

    cloudinary.config(
        cloud_name=ajustes.nube_cdn,
        api_key=ajustes.api_key_cdn,
        api_secret=ajustes.api_secret_cdn,
        secure=True,
    )


def subir_imagen(contenido: bytes, carpeta: str = "foodstore") -> dict[str, Any]:
    """Sube una imagen y devuelve su URL y public_id."""
    if not _cdn_disponible():
        identificador = f"{carpeta}/sim-{uuid.uuid4().hex[:12]}"
        return {
            "url": f"https://simulado.local/{identificador}.jpg",
            "id_cdn": identificador,
            "simulado": True,
        }

    import cloudinary.uploader

    _configurar()
    respuesta = cloudinary.uploader.upload(contenido, folder=carpeta)
    return {
        "url": respuesta.get("secure_url"),
        "id_cdn": respuesta.get("public_id"),
        "simulado": False,
    }


def eliminar_imagen(id_cdn: str) -> bool:
    """Elimina una imagen del CDN por su public_id."""
    if not _cdn_disponible():
        return True

    import cloudinary.uploader

    _configurar()
    respuesta = cloudinary.uploader.destroy(id_cdn)
    return respuesta.get("result") == "ok"
