from loguru import logger
from sqlalchemy.orm import Session

from db import database
from db.models.fundamental import *
from db.models.stock import Stock


class StockController:
    def __init__(self):
        self.db = database
        self.db.setup_db()
        self.session = Session(self.db.engine)

    def get_stock(self):
        for stock in Stock.all(self.session):
            logger.info(stock.ticker)

    def find_by_id(self, id: int):
        stock = Stock.find_by_id(self.session, id)
        logger.info(stock.ticker)

    def find_by_ticker(self, ticker: str):
        stock = Stock.find_by_ticker(self.session, ticker)
        logger.info(stock.fundamentals[0].solvency.current_ratio_quarter)

    def find_solvency(self, id: int):
        solvency = Solvency.find_by_id(self.session, id)
        logger.info(solvency.fundamental.stock.name)


if __name__ == "__main__":
    StockController().get_stock()
    StockController().find_by_id(1)
    StockController().find_by_ticker("DOSS")
    StockController().find_solvency(1)
