import json
import os

from dotenv import load_dotenv

from schemas.stock import Stock
from services.google_drive_service import GoogleDriveService
from utils.logger_config import logger

load_dotenv()


class Spreadsheet:
    def __init__(self, title: str):
        self.title = title
        self.google_drive_service = GoogleDriveService()
        self.spreadsheet_id = ""
        self._create()

    def _create(self):
        self.spreadsheet_id = self.google_drive_service.create_spreadsheet(
            title=self.title
        )

        google_drive_emails = json.loads(os.getenv("GOOGLE_DRIVE_EMAILS"))
        for google_drive_email in google_drive_emails:
            self.google_drive_service.add_drive_permission(
                self.spreadsheet_id, google_drive_email
            )

    def insert_stock(self, stocks: [Stock]):
        header = ["Ticker", "Name", "IPO Date", "Market Cap", "Board"]
        sheet_values = [header]
        for stock in stocks:
            row = [
                stock.ticker,
                stock.name,
                stock.ipo_date,
                stock.market_cap,
                stock.board,
            ]
            sheet_values.append(row)

        self.google_drive_service.insert_data(
            self.spreadsheet_id, "idx-stocks", sheet_values
        )
        logger.info(
            f"Stocks has been inserted on https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"
        )

    # def insert_fundamental(self, fundamentals: [Fundamental]):
    #     raise NotImplementedError("Need implementation")
