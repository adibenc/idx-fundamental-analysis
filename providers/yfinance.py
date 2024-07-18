import yfinance as yf
from utils.logger_config import logger


class YFinance:
    def __init__(self):
        self.yf = yf

    def info(self, stocks):
        for stock in stocks:
            info = self.yf.Ticker(stock.ticker).info
            logger.debug(info)
