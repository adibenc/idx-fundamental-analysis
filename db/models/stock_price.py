from sqlalchemy import String, Column, Float, BigInteger, ForeignKey

from db.models import BaseModel


class StockPrice(BaseModel):
    __tablename__ = "stock_price"

    price = Column(Float, default=0.0)
    volume = Column(BigInteger, default=0)
    change = Column(Float, default=0.0)
    percentage_change = Column(Float, default=0.0)
    average = Column(Float, default=0.0)
    close = Column(Float, default=0.0)
    high = Column(Float, default=0.0)
    low = Column(Float, default=0.0)
    open = Column(Float, default=0.0)
    ara = Column(Float, default=0.0)
    arb = Column(Float, default=0.0)
    frequency = Column(Float, default=0.0)
    fsell = Column(Float, default=0.0)
    fbuy = Column(Float, default=0.0)

    stock_ticker = Column(String, ForeignKey("stocks.ticker"))
