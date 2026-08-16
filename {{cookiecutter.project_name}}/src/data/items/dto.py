from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class ItemDTO(BaseModel):
    id: PositiveInt
    name: str
    description: str | None
    price: Annotated[Decimal, Field(max_digits=16, decimal_places=8, ge=0)]

    model_config = ConfigDict(from_attributes=True)


class ItemFilters(BaseModel):
    id: list[PositiveInt]
