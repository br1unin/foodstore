"""Gestor de conexiones WebSocket agrupadas por canal."""
from __future__ import annotations

from typing import Any, Iterable

from fastapi import WebSocket


class GestorConexiones:
    """Mantiene el conjunto de sockets activos por cada canal logico."""

    def __init__(self) -> None:
        self.canales: dict[str, set[WebSocket]] = {}

    async def conectar(self, ws: WebSocket, canal: str) -> None:
        """Registra un socket ya aceptado dentro de un canal."""
        self.canales.setdefault(canal, set()).add(ws)

    def desconectar(self, ws: WebSocket, canal: str) -> None:
        """Quita un socket del canal y limpia canales vacios."""
        suscriptores = self.canales.get(canal)
        if suscriptores is None:
            return
        suscriptores.discard(ws)
        if not suscriptores:
            self.canales.pop(canal, None)

    async def difundir(self, canal: str, mensaje: dict[str, Any]) -> None:
        """Envia un mensaje JSON a todos los sockets de un canal."""
        muertos: list[WebSocket] = []
        for ws in list(self.canales.get(canal, set())):
            try:
                await ws.send_json(mensaje)
            except Exception:
                muertos.append(ws)
        for ws in muertos:
            self.desconectar(ws, canal)

    async def difundir_multiples(
        self, canales: Iterable[str], mensaje: dict[str, Any]
    ) -> None:
        """Difunde el mismo mensaje a varios canales."""
        for canal in canales:
            await self.difundir(canal, mensaje)


# Instancia compartida a nivel de aplicacion.
gestor_conexiones = GestorConexiones()
