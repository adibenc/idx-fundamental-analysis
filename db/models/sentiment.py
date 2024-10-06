from sqlalchemy import Column, String, Float, DateTime, ForeignKey

from db.models import BaseModel


class Sentiment(BaseModel):
    __tablename__ = "sentiments"

    content = Column(String, default="")
    rate = Column(Float, default=0.0)
    category = Column(String, default="")
    posted_at = Column(DateTime)

    stock_ticker = Column(String, ForeignKey("stocks.ticker"))
