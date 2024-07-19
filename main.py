from datetime import date

from dotenv import load_dotenv

from builders.spreadsheet import Spreadsheet
from providers.idx import IDX
from providers.stockbit import StockBit
from utils.logger_config import logger

logger.info("IDX Composite Fundamental Analysis")

load_dotenv()

# Retrieve stocks from IDX
idx = IDX()
stocks = idx.stocks()
logger.info("Stocks: {}".format(stocks))
logger.info("Total Stocks: {}".format(len(stocks)))

# Process stocks key statistics from Stockbit
stock_bit = StockBit()
stock_fundamentals = stock_bit.fundamentals(stocks=stocks)
stock_with_price = stock_bit.with_stock_price(stocks=stocks)

# Insert processed data into Google Spreadsheet
sheet_title = f"IDX Fundamental Analysis {date.today().strftime("%d-%m-%Y")}"
spreadsheet = Spreadsheet(title=sheet_title)
spreadsheet.insert_analysis(fundamentals=stock_fundamentals)
spreadsheet.insert_stock(stocks=stock_with_price)
spreadsheet.insert_fundamental(fundamentals=stock_fundamentals)
