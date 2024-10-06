from dataclasses import dataclass
from typing import List

from schemas.fundamental import Fundamental
from schemas.key_analysis import KeyAnalysis
from schemas.sentiment import Sentiment


@dataclass
class Stock:
    ticker: str
    name: str = ""
    ipo_date: str = ""
    note: str = ""
    market_cap: float = 0.0
    price: float = 0.0
    volume: int = 0
    change: float = 0.0
    percentage_change: float = 0.0
    average: float = 0.0
    close: float = 0.0
    high: float = 0.0
    low: float = 0.0
    open: float = 0.0
    ara: float = 0.0
    arb: float = 0.0
    frequency: float = 0.0
    fsell: float = 0.0
    fbuy: float = 0.0
    home_page: str = ""
    sentiment: List[Sentiment] = None
    fundamental: Fundamental = None
    key_analysis: KeyAnalysis = None
