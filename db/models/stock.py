from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import Relationship

from db.models import BaseModel


class Stock(BaseModel):
    __tablename__ = "stocks"

    ticker = Column(String)
    name = Column(String, default="")
    ipo_date = Column(String, default="")
    note = Column(String, default="")
    market_cap = Column(Float, default=0.0)
    price = Column(Float, default=0.0)
    volume = Column(Integer, default=0)
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
    home_page = Column(String, default="")

    fundamental = Relationship("Fundamental", backref="stock")
    sentiments = Relationship("Sentiment", backref="stock")
    key_analysis = Relationship("KeyAnalysis", backref="stock")
