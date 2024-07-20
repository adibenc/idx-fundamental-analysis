import argparse
from datetime import date

from dotenv import load_dotenv

from builders.fundamental_analyser import FundamentalAnalyser
from builders.spreadsheet import Spreadsheet
from providers.idx import IDX
from providers.stockbit import StockBit
from utils.logger_config import logger


def main():
    parser = argparse.ArgumentParser(description="IDX Composite Fundamental Analysis")
    parser.add_argument(
        "--full-retrieve", action="store_true", help="Retrieve full stock data from IDX"
    )
    args = parser.parse_args()

    logger.info("IDX Composite Fundamental Analysis")

    load_dotenv()

    # Retrieve stocks from IDX
    idx = IDX(is_full_retrieve=args.full_retrieve)
    stocks = idx.stocks()
    logger.info("Stocks: {}".format(stocks))
    logger.info("Total Stocks: {}".format(len(stocks)))

    # Process stocks key statistics from Stockbit
    stock_bit = StockBit(stocks=stocks).with_stock_price()
    stock_fundamentals = stock_bit.fundamentals()

    # Analyser
    fundamental_analyser = FundamentalAnalyser(fundamentals=stock_fundamentals)

    # Insert processed data into Google Spreadsheet
    sheet_title = f"IDX Fundamental Analysis {date.today().strftime('%d-%m-%Y')}"
    spreadsheet = Spreadsheet(
        title=sheet_title, fundamental_analyser=fundamental_analyser
    )
    spreadsheet.insert_analysis()
    spreadsheet.insert_stock()
    spreadsheet.insert_key_statistic()


if __name__ == "__main__":
    main()
