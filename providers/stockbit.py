import os
import time

import requests
from dotenv import load_dotenv

from schemas.fundamental import Fundamental
from schemas.stock import Stock
from utils.helpers import parse_currency_to_float
from utils.logger_config import logger

load_dotenv()


class StockBit:
    """
    A class to interact with the StockBit API and fetch key statistics for stocks.

    Attributes:
        url (str): The base URL for the StockBit API.
        request_headers (dict): Headers to be used in the API requests.
        response_data (dict): Data received from the API response.

    Methods:
        key_stats(stocks: [Stock]):
            Fetches key statistics for a list of stocks and logs the data.

        _fundamental(stock: Stock) -> Fundamental:
            Parses the API response data and returns a Fundamental object.
    """

    def __init__(self):
        """
        Initializes the StockBit provider with necessary headers and URL.
        """
        logger.info("StockBit provider initialised")
        self.url = "https://exodus.stockbit.com/keystats/ratio/v1/{}?year_limit=10"
        self.request_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://stockbit.com/",
            "Authorization": f'Bearer {os.getenv("STOCKBIT_JWT_TOKEN")}',
            "Origin": "https://stockbit.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "TE": "trailers",
        }
        self.response_data = None

    def key_stats(self, stocks: [Stock]) -> [Fundamental]:
        """
        Fetches key statistics for a list of stocks and logs the data.

        Args:
            stocks (list of Stock): List of Stock objects to fetch statistics for.

        Returns:
            [Fundamental]: list of Fundamental object containing parsed fundamental data.
        """
        fundamentals = []
        for stock in stocks:
            url = self.url.format(stock.ticker)

            try:
                response = requests.get(url, headers=self.request_headers)
                if response.status_code == 200:
                    self.response_data = response.json()

                    fundamental = self._fundamental(stock)
                    fundamentals.append(fundamental)
                else:
                    logger.error(
                        f"Error: Received status code {response.status_code} - {response.text}"
                    )

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")

            time.sleep(0.2)

        return fundamentals

    def _fundamental(self, stock: Stock) -> Fundamental:
        """
        Parses the API response data and returns a Fundamental object.

        Args:
            stock (Stock): The Stock object for which the fundamental data is being parsed.

        Returns:
            Fundamental: An object containing parsed fundamental data.
        """
        fundamental = Fundamental()
        fundamental.stock = stock

        # Stats
        #
        stats = self.response_data["data"]["stats"]
        fundamental.stats.current_share_outstanding = parse_currency_to_float(
            stats["current_share_outstanding"]
        )
        fundamental.stats.market_cap = parse_currency_to_float(stats["market_cap"])
        fundamental.stats.enterprise_value = parse_currency_to_float(
            stats["enterprise_value"]
        )

        # Current Valuation
        #
        closure_fin_items_results = self.response_data["data"][
            "closure_fin_items_results"
        ]
        current_valuation_fin_name_results = closure_fin_items_results[0][
            "fin_name_results"
        ]
        fundamental.current_valuation.current_pe_ratio_annual = float(
            current_valuation_fin_name_results[0]["fitem"]["value"]
        )
        fundamental.current_valuation.current_pe_ratio_ttm = float(
            current_valuation_fin_name_results[1]["fitem"]["value"]
        )
        fundamental.current_valuation.current_price_to_sales_ttm = float(
            current_valuation_fin_name_results[2]["fitem"]["value"]
        )

        return fundamental
