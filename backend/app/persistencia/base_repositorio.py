"""Repositorio base generico con operaciones comunes de persistencia."""
from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlmodel import Session, SQLModel

T = TypeVar("T", bound=SQLModel)
E = TypeVar("E", bound=SQLModel)


class BaseRepositorio(Generic[T]):
    def __init__(self, sesion: Session) -> None:
        self.sesion = sesion

    def guardar(self, entidad: E) -> E:
        """Persiste una entidad y sincroniza la sesion."""
        self.sesion.add(entidad)
        self.sesion.flush()
        return entidad

    def eliminar(self, entidad: Any) -> None:
        """Elimina una entidad de la base de datos."""
        self.sesion.delete(entidad)
        self.sesion.flush()
