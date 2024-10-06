from sqlalchemy import Column, String, Float
from sqlalchemy.orm import Relationship

from db.models import BaseModel


class Stock(BaseModel):
    __tablename__ = "stocks"

    ticker = Column(String, index=True, nullable=False, unique=True)
    name = Column(String, default="")
    ipo_date = Column(String, default="")
    note = Column(String, default="")
    market_cap = Column(Float, default=0.0)
    home_page = Column(String, default="")

    stock_price = Relationship("StockPrice", backref="stock")
    fundamental = Relationship("Fundamental", backref="stock")
    sentiments = Relationship("Sentiment", backref="stock")
    key_analysis = Relationship("KeyAnalysis", backref="stock")
