from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel

class Componente(SQLModel, table=True):

    __tablename__ = "componente"

    id: Optional[int] = Field(default=None, primary_key=True)
    denominacion: str = Field(max_length=100, index=True)
    existencias: int = Field(default=0)
    precio_unitario: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=10)
    genera_alergia: bool = Field(default=False)
    eliminado_en: Optional[datetime] = Field(default=None)
