"""Unidad de trabajo (Unit of Work) sobre una sesion de base de datos."""
from __future__ import annotations

from types import TracebackType
from typing import Any, Generator

from sqlmodel import Session

from app.persistencia.motor import motor


class GestorTransaccion:
    """Encapsula el ciclo de vida transaccional de una sesion.

    Las capas de servicio operan sobre esta unidad de trabajo pero nunca
    confirman directamente: el commit lo realiza ``obtener_gestor`` al cerrar
    la peticion, o bien el enrutador usando ``with gestor:`` cuando necesita
    emitir notificaciones WebSocket posteriores al commit.
    """

    def __init__(self, sesion: Session) -> None:
        self.sesion = sesion
        self._confirmado = False

    # --- Context manager -------------------------------------------------

    def __enter__(self) -> "GestorTransaccion":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is None:
            self.confirmar()
        else:
            self.revertir()

    # --- Operaciones transaccionales -------------------------------------

    def confirmar(self) -> None:
        """Persiste de forma definitiva los cambios pendientes."""
        self.sesion.commit()
        self._confirmado = True

    def revertir(self) -> None:
        """Descarta los cambios pendientes."""
        self.sesion.rollback()

    def sincronizar(self) -> None:
        """Vuelca los cambios a la base sin cerrar la transaccion."""
        self.sesion.flush()

    def actualizar(self, instancia: Any) -> None:
        """Refresca una instancia con el estado persistido."""
        self.sesion.refresh(instancia)


def obtener_gestor() -> Generator[GestorTransaccion, None, None]:
    """Dependencia FastAPI que entrega una unidad de trabajo por peticion."""
    with Session(motor) as sesion:
        gestor = GestorTransaccion(sesion)
        try:
            yield gestor
            gestor.confirmar()
        except Exception:
            gestor.revertir()
            raise
