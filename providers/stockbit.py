import os
import tempfile
import time

import requests
from dotenv import load_dotenv

from schemas.fundamental import (
    Fundamental,
    PerShare,
    Solvency,
    ManagementEffectiveness,
    Profitability,
    Growth,
    Dividend,
    MarketRank,
    IncomeStatement,
    BalanceSheet,
    CashFlowStatement,
    PricePerformance,
    CurrentValuation,
    Stats,
)
from schemas.stock import Stock
from utils.helpers import (
    parse_currency_to_float,
    parse_key_statistic_results_item_value,
)
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
        self.request_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.token = ""
        self.token_temp_file_path = os.path.join(
            tempfile.gettempdir(), "stockbit-token.tmp"
        )
        self._read_token()

        self.key_statistic = None

    def authenticate(self, username, password):
        """
        Authenticates a user by sending a POST request to the login API with the provided username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Raises:
            requests.exceptions.RequestException: If the request fails due to network issues or invalid URL.

        Side Effects:
            - Sets the `self.token` attribute with the access token received from the API response if authentication is successful.
            - Writes the access token to a temporary file specified by `self.token_temp_file_path`.
            - Logs an error message if the response status code is not 200 or if the request fails.
        """
        url = "https://stockbit.com/api/login/email"
        payload = {"username": username, "password": password}

        try:
            response = requests.post(url, headers=self.request_headers, json=payload)

            if response.status_code == 200:
                self.token = response.json()["data"]["access"]["token"]

                with open(self.token_temp_file_path, "w") as file:
                    file.write(self.token)

            else:
                logger.error(
                    f"Error: Received status code {response.status_code} - {response.text}"
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")

    def _read_token(self):
        """
        Reads the authentication token from a temporary file and sets it to `self.token`.

        Raises:
            FileNotFoundError: If the token file does not exist, triggers the authentication process to generate the token.
            IOError: If an I/O error occurs while reading the file, logs an error message.

        Side Effects:
            - Sets the `self.token` attribute with the token read from the file.
            - Logs an informational message if the token file is not found and initiates the authentication process.
            - Logs an error message if an I/O error occurs while reading the file.
        """
        try:
            with open(self.token_temp_file_path, "r") as file:
                self.token = file.read()
        except FileNotFoundError as e:
            logger.info(
                f"Will generate stockbit-token file once and authenticate for the first time"
                f"{self.token_temp_file_path}"
            )
            self.authenticate(
                username=os.getenv("STOCKBIT_USERNAME"),
                password=os.getenv("STOCKBIT_PASSWORD"),
            )
        except IOError as e:
            logger.error(f"An error occurred while reading from the file: {e}")

    def key_statistic_by_stock(self, stock: Stock) -> dict:
        """
        Retrieves key statistics for a given stock by sending a GET request to the API.

        Args:
            stock (Stock): An instance of the Stock class containing the ticker symbol.

        Returns:
            dict: A dictionary containing the key statistics if the request is successful.
            None: If the request fails after retrying or encounters an error.

        Raises:
            requests.exceptions.RequestException: If the request fails due to network issues or invalid URL.

        Side Effects:
            - Logs an error message if the response status code is not 200.
            - Re-authenticates if a 401 Unauthorized status code is received and retries the request up to 3 times.
            - Logs an error message if the request fails due to an exception.
            - Logs an informational message if the request fails after all retries.
        """
        url = f"https://exodus.stockbit.com/keystats/ratio/v1/{stock.ticker}?year_limit=10"
        retry = 0

        while retry <= 3:
            try:
                headers = self.request_headers
                headers["Authorization"] = f"Bearer {self.token}"
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(
                        f"Error: Received status code {response.status_code}, "
                        f"text: {response.text}, "
                        f"ticker: {stock.ticker}, "
                        f"retry: {retry}"
                    )

                    if response.status_code == 401:
                        self.authenticate(
                            username=os.getenv("STOCKBIT_USERNAME"),
                            password=os.getenv("STOCKBIT_PASSWORD"),
                        )
                        retry += 1
                    else:
                        break

            except requests.exceptions.RequestException as e:
                logger.error(
                    f"Request failed: {e} "
                    f"ticker: {stock.ticker}, "
                    f"retry: {retry}"
                )
                break

            time.sleep(0.2)

        logger.info(
            "Failed to retrieve key statistics "
            f"ticker: {stock.ticker}, "
            f"retry: {retry}"
        )
        return None

    def fundamentals(self, stocks: [Stock]) -> [Fundamental]:
        """
        Get fundamentals for a list of stocks.

        Args:
            stocks (list of Stock): List of Stock objects to fetch statistics for.

        Returns:
            [Fundamental]: list of Fundamental object containing parsed fundamental data.
        """
        fundamentals = []
        for stock in stocks:
            self.key_statistic = self.key_statistic_by_stock(stock)

            if self.key_statistic:
                fundamentals.append(self._fundamental(stock))

            time.sleep(0.2)

        return fundamentals

    def _fundamental(self, stock: Stock) -> Fundamental | None:
        """
        Parses the API response data and returns a Fundamental object.

        Args:
            stock (Stock): The Stock object for which the fundamental data is being parsed.

        Returns:
            Fundamental: An object containing parsed fundamental data.
        """

        if self.key_statistic == {}:
            return None

        fundamental = Fundamental()
        fundamental.stock = stock

        data = self.key_statistic["data"]

        # Stats
        #
        stats = Stats(
            parse_currency_to_float(data["stats"]["current_share_outstanding"]),
            parse_currency_to_float(data["stats"]["market_cap"]),
            parse_currency_to_float(data["stats"]["enterprise_value"]),
        )
        fundamental.stats = stats
        logger.debug(stats)

        # -- nested object
        closure_fin_items_results = data["closure_fin_items_results"]

        # Current Valuation
        #
        current_valuation_fin_name_results = closure_fin_items_results[0][
            "fin_name_results"
        ]

        current_valuation = CurrentValuation(
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 0
            ),
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 1
            ),
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 2
            ),
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 3
            ),
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 4
            ),
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 5
            ),
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 6
            ),
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 7
            ),
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 8
            ),
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 9
            ),
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 10
            ),
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 11
            ),
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 12
            ),
            parse_key_statistic_results_item_value(
                current_valuation_fin_name_results, 13
            ),
        )
        fundamental.current_valuation = current_valuation
        logger.debug(current_valuation)

        # Per Share
        #
        per_share_fin_name_results = closure_fin_items_results[1]["fin_name_results"]
        per_share = PerShare(
            parse_key_statistic_results_item_value(per_share_fin_name_results, 0),
            parse_key_statistic_results_item_value(per_share_fin_name_results, 1),
            parse_key_statistic_results_item_value(per_share_fin_name_results, 2),
            parse_key_statistic_results_item_value(per_share_fin_name_results, 3),
            parse_key_statistic_results_item_value(per_share_fin_name_results, 4),
            parse_key_statistic_results_item_value(per_share_fin_name_results, 5),
        )
        fundamental.per_share = per_share
        logger.debug(per_share)

        # Solvency
        #
        solvency_fin_name_results = closure_fin_items_results[2]["fin_name_results"]
        solvency = Solvency(
            parse_key_statistic_results_item_value(solvency_fin_name_results, 0),
            parse_key_statistic_results_item_value(solvency_fin_name_results, 1),
            parse_key_statistic_results_item_value(solvency_fin_name_results, 2),
            parse_key_statistic_results_item_value(solvency_fin_name_results, 3),
            parse_key_statistic_results_item_value(solvency_fin_name_results, 4),
            parse_key_statistic_results_item_value(solvency_fin_name_results, 5),
            parse_key_statistic_results_item_value(solvency_fin_name_results, 6),
            parse_key_statistic_results_item_value(solvency_fin_name_results, 7),
            parse_key_statistic_results_item_value(solvency_fin_name_results, 8),
            parse_key_statistic_results_item_value(solvency_fin_name_results, 9),
        )
        fundamental.solvency = solvency
        logger.debug(solvency)

        # Management Effectivieness
        management_effectiveness_fin_name_results = closure_fin_items_results[3][
            "fin_name_results"
        ]
        management_effectiveness = ManagementEffectiveness(
            parse_key_statistic_results_item_value(
                management_effectiveness_fin_name_results, 0
            ),
            parse_key_statistic_results_item_value(
                management_effectiveness_fin_name_results, 1
            ),
            parse_key_statistic_results_item_value(
                management_effectiveness_fin_name_results, 2
            ),
            parse_key_statistic_results_item_value(
                management_effectiveness_fin_name_results, 3
            ),
            parse_key_statistic_results_item_value(
                management_effectiveness_fin_name_results, 4
            ),
            parse_key_statistic_results_item_value(
                management_effectiveness_fin_name_results, 5
            ),
            parse_key_statistic_results_item_value(
                management_effectiveness_fin_name_results, 6
            ),
            parse_key_statistic_results_item_value(
                management_effectiveness_fin_name_results, 7
            ),
            parse_key_statistic_results_item_value(
                management_effectiveness_fin_name_results, 8
            ),
            parse_key_statistic_results_item_value(
                management_effectiveness_fin_name_results, 9
            ),
            parse_key_statistic_results_item_value(
                management_effectiveness_fin_name_results, 10
            ),
        )
        fundamental.management_effectiveness = management_effectiveness
        logger.debug(management_effectiveness)

        # Profitability
        #
        profitability_fin_name_results = closure_fin_items_results[4][
            "fin_name_results"
        ]
        profitability = Profitability(
            parse_key_statistic_results_item_value(profitability_fin_name_results, 0),
            parse_key_statistic_results_item_value(profitability_fin_name_results, 1),
            parse_key_statistic_results_item_value(profitability_fin_name_results, 2),
        )
        fundamental.profitability = profitability
        logger.debug(profitability)

        # Growth
        #
        growth_fin_name_results = closure_fin_items_results[5]["fin_name_results"]
        growth = Growth(
            parse_key_statistic_results_item_value(growth_fin_name_results, 0),
            parse_key_statistic_results_item_value(growth_fin_name_results, 1),
            parse_key_statistic_results_item_value(growth_fin_name_results, 2),
        )
        fundamental.growth = growth
        logger.debug(growth)

        # Dividend
        #
        dividend_fin_name_results = closure_fin_items_results[6]["fin_name_results"]
        dividend = Dividend(
            parse_key_statistic_results_item_value(dividend_fin_name_results, 0),
            parse_key_statistic_results_item_value(dividend_fin_name_results, 1),
            parse_key_statistic_results_item_value(dividend_fin_name_results, 2),
            parse_key_statistic_results_item_value(dividend_fin_name_results, 3),
            parse_key_statistic_results_item_value(dividend_fin_name_results, 4),
        )
        fundamental.dividend = dividend
        logger.debug(dividend)

        # Market Rank
        #
        market_rank_fin_name_results = closure_fin_items_results[7]["fin_name_results"]
        market_rank = MarketRank(
            parse_key_statistic_results_item_value(market_rank_fin_name_results, 0),
            parse_key_statistic_results_item_value(market_rank_fin_name_results, 1),
            parse_key_statistic_results_item_value(market_rank_fin_name_results, 2),
            parse_key_statistic_results_item_value(market_rank_fin_name_results, 3),
            parse_key_statistic_results_item_value(market_rank_fin_name_results, 4),
            parse_key_statistic_results_item_value(market_rank_fin_name_results, 5),
            parse_key_statistic_results_item_value(market_rank_fin_name_results, 6),
            parse_key_statistic_results_item_value(market_rank_fin_name_results, 7),
            parse_key_statistic_results_item_value(market_rank_fin_name_results, 8),
        )
        fundamental.market_rank = market_rank
        logger.debug(market_rank)

        # Income Statement
        #
        income_statement_fin_name_results = closure_fin_items_results[8][
            "fin_name_results"
        ]
        income_statement = IncomeStatement(
            parse_key_statistic_results_item_value(
                income_statement_fin_name_results, 0
            ),
            parse_key_statistic_results_item_value(
                income_statement_fin_name_results, 1
            ),
            parse_key_statistic_results_item_value(
                income_statement_fin_name_results, 2
            ),
            parse_key_statistic_results_item_value(
                income_statement_fin_name_results, 3
            ),
        )
        fundamental.income_statement = income_statement
        logger.debug(income_statement)

        # Balance Sheet
        #
        balance_sheet_fin_name_results = closure_fin_items_results[9][
            "fin_name_results"
        ]
        balance_sheet = BalanceSheet(
            parse_key_statistic_results_item_value(balance_sheet_fin_name_results, 0),
            parse_key_statistic_results_item_value(balance_sheet_fin_name_results, 1),
            parse_key_statistic_results_item_value(balance_sheet_fin_name_results, 2),
            parse_key_statistic_results_item_value(balance_sheet_fin_name_results, 3),
            parse_key_statistic_results_item_value(balance_sheet_fin_name_results, 4),
            parse_key_statistic_results_item_value(balance_sheet_fin_name_results, 5),
            parse_key_statistic_results_item_value(balance_sheet_fin_name_results, 6),
            parse_key_statistic_results_item_value(balance_sheet_fin_name_results, 7),
            parse_key_statistic_results_item_value(balance_sheet_fin_name_results, 8),
        )
        fundamental.balance_sheet = balance_sheet
        logger.debug(balance_sheet)

        # Cash Flow
        #
        cash_flow_statement_fin_name_results = closure_fin_items_results[10][
            "fin_name_results"
        ]
        cash_flow_statement = CashFlowStatement(
            parse_key_statistic_results_item_value(
                cash_flow_statement_fin_name_results, 0
            ),
            parse_key_statistic_results_item_value(
                cash_flow_statement_fin_name_results, 1
            ),
            parse_key_statistic_results_item_value(
                cash_flow_statement_fin_name_results, 2
            ),
            parse_key_statistic_results_item_value(
                cash_flow_statement_fin_name_results, 3
            ),
            parse_key_statistic_results_item_value(
                cash_flow_statement_fin_name_results, 4
            ),
        )
        fundamental.cash_flow_statement = cash_flow_statement
        logger.debug(cash_flow_statement)

        # Price Performance
        #
        price_performance_fin_name_results = closure_fin_items_results[11][
            "fin_name_results"
        ]
        price_performance = PricePerformance(
            parse_key_statistic_results_item_value(
                price_performance_fin_name_results, 0
            ),
            parse_key_statistic_results_item_value(
                price_performance_fin_name_results, 1
            ),
            parse_key_statistic_results_item_value(
                price_performance_fin_name_results, 2
            ),
            parse_key_statistic_results_item_value(
                price_performance_fin_name_results, 3
            ),
            parse_key_statistic_results_item_value(
                price_performance_fin_name_results, 4
            ),
            parse_key_statistic_results_item_value(
                price_performance_fin_name_results, 5
            ),
            parse_key_statistic_results_item_value(
                price_performance_fin_name_results, 6
            ),
            parse_key_statistic_results_item_value(
                price_performance_fin_name_results, 7
            ),
            parse_key_statistic_results_item_value(
                price_performance_fin_name_results, 8
            ),
            parse_key_statistic_results_item_value(
                price_performance_fin_name_results, 9
            ),
            parse_key_statistic_results_item_value(
                price_performance_fin_name_results, 10
            ),
        )
        fundamental.price_performance = price_performance
        logger.debug(price_performance)

        logger.debug(fundamental)
        return fundamental

    def stock_price(self, stock: Stock) -> Stock:
        """
        Retrieves stock prices for a given stock by sending a GET request to the API.

        Args:
            stock (Stock): An instance of the Stock class containing the ticker symbol.

        Returns:
           stock

        Raises:
            requests.exceptions.RequestException: If the request fails due to network issues or invalid URL.

        Side Effects:
            - Logs an error message if the response status code is not 200.
            - Re-authenticates if a 401 Unauthorized status code is received and retries the request up to 3 times.
            - Logs an error message if the request fails due to an exception.
            - Logs an informational message if the request fails after all retries.
        """

        url = f"https://exodus.stockbit.com/company-price-feed/v2/orderbook/companies/{stock.ticker}"
        headers = self.request_headers
        headers["Authorization"] = f"Bearer {self.token}"

        retry = 0

        while retry <= 3:
            try:
                headers = self.request_headers
                headers["Authorization"] = f"Bearer {self.token}"
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    data = response.json()["data"]
                    stock.price = data["lastprice"]
                    stock.change = data["change"]
                    stock.fbuy = data["fbuy"]
                    stock.fsell = data["fsell"]
                    stock.volume = data["volume"]
                    stock.percentage_change = data["percentage_change"]
                    stock.average = data["average"]
                    stock.close = data["close"]
                    stock.high = data["high"]
                    stock.low = data["low"]
                    stock.open = data["open"]
                    stock.ara = float(data["ara"]["value"].replace(",", ""))
                    stock.arb = float(data["arb"]["value"].replace(",", ""))
                    stock.frequency = data["frequency"]
                    return stock

                else:
                    logger.error(
                        f"Error: Received status code {response.status_code}, "
                        f"text: {response.text}, "
                        f"ticker: {stock.ticker}, "
                        f"retry: {retry}"
                    )

                    if response.status_code == 401:
                        self.authenticate(
                            username=os.getenv("STOCKBIT_USERNAME"),
                            password=os.getenv("STOCKBIT_PASSWORD"),
                        )
                        retry += 1
                    else:
                        break

            except requests.exceptions.RequestException as e:
                logger.error(
                    f"Request failed: {e} "
                    f"ticker: {stock.ticker}, "
                    f"retry: {retry}"
                )
                break

            time.sleep(0.2)

        logger.info(
            "Failed to retrieve prices data "
            f"ticker: {stock.ticker}, "
            f"retry: {retry}"
        )

        return stock

    def with_stock_price(self, stocks: [Stock]) -> [Stock]:
        """
        Get stock prices for a list of stocks.

        Args:
            stocks (list of Stock): List of Stock objects to fetch statistics for.

        Returns:
            [Fundamental]: list of Fundamental object containing parsed fundamental data.
        """
        stock_prices = []
        for stock in stocks:
            stock_prices.append(self.stock_price(stock))

            time.sleep(0.2)

        return stock_prices
