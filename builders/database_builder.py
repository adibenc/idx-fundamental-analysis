from builders.builder_interface import BuilderInterface
from db.models.stock import Stock

from db.session import get_session
from schemas.stock import Stock as StockSchema


class DatabaseBuilder(BuilderInterface):
    def __init__(self, stocks=[StockSchema]):
        self.stocks = stocks

    def insert_stock(self):
        for stock in self.stocks:
            with get_session() as session:
                stock_model = Stock(
                    ticker=stock.ticker,
                    name=stock.name,
                    ipo_date=stock.ipo_date,
                    note=stock.note,
                    market_cap=stock.market_cap,
                    price=stock.price,
                    volume=stock.volume,
                    change=stock.change,
                    percentage_change=stock.percentage_change,
                    average=stock.average,
                    close=stock.close,
                    high=stock.high,
                    low=stock.low,
                    ara=stock.ara,
                    arb=stock.arb,
                    frequency=stock.frequency,
                    fsell=stock.fsell,
                    home_page=stock.home_page,
                )

                session.add(stock_model)

    def insert_key_statistic(self):
        pass

    def insert_analysis(self):
        pass

    def insert_sentiment(self):
        pass
