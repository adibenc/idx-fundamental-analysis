from dataclasses import dataclass


@dataclass
class Stock:
    ticker: str
    name: str
    ipo_date: str
    board: str
    market_cap: float
    price: float = 0.0
    volume: int = 0
    change: float = 0.0
    percentage_change: float = 0.0
