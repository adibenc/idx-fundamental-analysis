import argparse
from datetime import date

from dotenv import load_dotenv

from builders.excel import Excel
from builders.fundamental_analyser import FundamentalAnalyser
from builders.spreadsheet import Spreadsheet
from providers.idx import IDX
from providers.stockbit import StockBit
from utils.logger_config import logger


def main():
    parser = argparse.ArgumentParser(description="IDX Composite Fundamental Analysis")
    parser.add_argument(
        "-f",
        "--full-retrieve",
        action="store_true",
        help="Retrieve full stock data from IDX",
    )
    parser.add_argument(
        "-o",
        "--output-format",
        choices=["spreadsheet", "excel"],
        default="spreadsheet",
        help="Specify the output format: 'spreadsheet' for Google Spreadsheet, 'excel' for Excel file",
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

    sheet_title = f"IDX Fundamental Analysis {date.today().strftime('%d-%m-%Y')}"
    if args.output_format == "spreadsheet":
        # Insert processed data into Google Spreadsheet
        spreadsheet = Spreadsheet(
            title=sheet_title, fundamental_analyser=fundamental_analyser
        )
        spreadsheet.insert_analysis()
        spreadsheet.insert_stock()
        spreadsheet.insert_key_statistic()
    elif args.output_format == "excel":
        # Insert processed data into local Excel file
        excel_file = f"{sheet_title}.xlsx"
        excel = Excel(filename=excel_file, fundamental_analyser=fundamental_analyser)
        excel.insert_analysis()
        excel.insert_stock()
        excel.insert_key_statistic()
        excel.save()
    else:
        logger.error("Invalid output format specified.")


if __name__ == "__main__":
    main()
