from decimal import Decimal

from sqlalchemy import String, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2048))
    price: Mapped[Decimal] = mapped_column(Numeric(16, 8), nullable=False)

    def __repr__(self) -> str:
        return f"<Item id={self.id} name={self.name} price={self.price}>"
