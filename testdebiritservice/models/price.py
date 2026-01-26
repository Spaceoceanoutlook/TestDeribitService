from testdebiritservice.models import Base
from sqlalchemy import String, Integer, Numeric, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(String, index=True, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
