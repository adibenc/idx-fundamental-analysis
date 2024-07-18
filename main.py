from datetime import date

from dotenv import load_dotenv

from builders.spreadsheet import Spreadsheet
from providers.idx import IDX
from providers.stockbit import StockBit
from utils.logger_config import logger

logger.info("IDX Composite Fundamental Analysis")

load_dotenv()

idx = IDX()
stocks = idx.stocks()
logger.info("Stocks: {}".format(stocks))
logger.info("Total Stocks: {}".format(len(stocks)))

# TODO: Insert into spreadsheet
sheet_title = f"IDX Fundamental Analysis {date.today().strftime("%d-%m-%Y")}"
spreadsheet = Spreadsheet(title=sheet_title)
spreadsheet.insert_stock(stocks)

# TODO: Retrieve Stock key statistics from Stockbit
stock_bit = StockBit()
stock_bit.key_stats(stocks)
