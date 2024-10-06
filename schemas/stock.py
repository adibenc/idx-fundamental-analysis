from dataclasses import dataclass
from typing import List

from schemas import BaseDataClass
from schemas.fundamental import Fundamental
from schemas.key_analysis import KeyAnalysis
from schemas.sentiment import Sentiment
from schemas.stock_price import StockPrice


@dataclass
class Stock(BaseDataClass):
    ticker: str
    name: str = ""
    ipo_date: str = ""
    note: str = ""
    market_cap: float = 0.0
    home_page: str = ""
    stock_price: StockPrice = None
    sentiment: List[Sentiment] = None
    fundamental: Fundamental = None
    key_analysis: KeyAnalysis = None
