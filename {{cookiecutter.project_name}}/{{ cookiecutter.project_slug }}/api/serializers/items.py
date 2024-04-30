from typing import Optional

from pydantic import BaseModel


class ItemRequest(BaseModel):
    name: str
    description: Optional[str] = None
    price: int


class ItemResponse(ItemRequest):
    id: int
