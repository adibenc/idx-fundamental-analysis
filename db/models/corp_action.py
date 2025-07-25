from sqlalchemy import ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db import BaseModel

class CorpAction(BaseModel):
    __tablename__ = "corp_actions"

    stock_ticker: Mapped[str] = mapped_column(String, ForeignKey("stocks.ticker"))
    company_id: Mapped[int]
    company_symbol: Mapped[str]
    rups_date: Mapped[DateTime]
    rups_venue: Mapped[str]
    rups_time: Mapped[str]

    stock: Mapped["Stock"] = relationship(back_populates="corp_actions")
