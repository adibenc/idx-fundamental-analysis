import os
import tempfile
import time

import requests

from utils.logger_config import logger


class StockbitApiClient:
    """
    Handles HTTP requests to the Stockbit API, including authentication and retries.
    """

    def __init__(self):
        """
        Initializes the StockbitHttpRequest with a URL and optional headers.
        Authenticates with the Stockbit API upon initialization.

        Parameters:
        - headers (dict): Optional headers for the HTTP request.
        """
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        self.is_authorise = False

        self.token_temp_file_path = os.path.join(tempfile.gettempdir(), "tokennn.tmp")

        self.refresh_token_temp_file_path = os.path.join(
            tempfile.gettempdir(), "refresh_tokennn.tmp"
        )

        self._initialize_token_file()

    def _request(self, url: str, method: str, payload: dict = None):
        """
        Makes an HTTP request with the specified method and payload, retrying on failure.

        Parameters:
        - method (str): The HTTP method ("GET" or "POST").
        - payload (dict): Optional payload for POST requests.

        Returns:
        - dict: The JSON response from the server, or an empty dictionary on failure.
        """
        retry = 0
        while retry <= 3:
            try:
                if method == "GET":
                    response = requests.get(url, headers=self.headers)
                elif method == "POST":
                    response = requests.post(url, headers=self.headers, json=payload)
                else:
                    raise ValueError("Unsupported HTTP method")

                logger.debug(url)
                logger.debug(response.status_code)
                logger.debug(response.json())

                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(
                        f"Error: Received status code {response.status_code}, "
                        f"text: {response.text}, "
                        f"retry: {retry}"
                    )
                    if response.status_code == 401:
                        self._authenticate_stockbit()
                        retry += 1
                    else:
                        break

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e} retry: {retry}")
                break

            time.sleep(0.2)

        logger.error(f"Failed to retrieve key statistics retry: {retry}")
        return {}

    def get(self, url: str):
        """
        Performs a GET request using the stored URL and headers.

        Returns:
        - dict: The JSON response from the server, or an empty dictionary on failure.
        """
        return self._request(url, "GET")

    def post(self, url: str, payload: dict):
        """
        Performs a POST request using the stored URL, headers, and provided payload.

        Parameters:
        - payload (dict): The payload for the POST request.

        Returns:
        - dict: The JSON response from the server, or an empty dictionary on failure.
        """
        return self._request(url, "POST", payload)

    def _authenticate_stockbit(self):
        """
        Authenticates with the Stockbit API and updates the authorization header.
        Get refresh token if the token is expired
        Login if needed
        """

        if self.is_authorise and not self._is_refresh_token_empty():
            self._refresh_token()
        else:
            self._login()

    def _login(self):
        """
        Login to Stockbit API.
        """
        url = "https://api.stockbit.com/v2.5/login"

        params = {
            "user": os.getenv("STOCKBIT_USERNAME"),
            "password": os.getenv("STOCKBIT_PASSWORD"),
        }

        self.headers["Authorization"] = None

        try:
            response = requests.post(url, headers=self.headers, params=params)

            if response.status_code == 200:
                logger.info("Logged in successfully with username and password!")

                token = response.json()["data"]["access_token"]
                refresh_token = response.json()["data"]["refresh_token"]

                self.headers["Authorization"] = f"Bearer {token}"

                self._write_token(token, refresh_token)

                self.is_authorise = True
            else:
                logger.error(
                    f"Error: Received status code {response.status_code} - {response.text}"
                )
                self.is_authorise = False

            time.sleep(1)

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        except KeyError as e:
            logger.error(f"Key error: {e}")

    def _refresh_token(self):
        """
        Refreshes new token using refresh token.
        """
        url = "https://exodus.stockbit.com/login/refresh"

        with open(self.refresh_token_temp_file_path, "r") as file:
            self.headers["Authorization"] = f"Bearer {file.read()}"

            try:
                response = requests.post(url, headers=self.headers)

                if response.status_code == 200:
                    logger.info("Token is successfully refreshed!")

                    token = response.json()["data"]["access"]["token"]
                    refresh_token = response.json()["data"]["refresh"]["token"]

                    self.headers["Authorization"] = f"Bearer {token}"

                    self._write_token(token, refresh_token)

                    self.is_authorise = True
                else:
                    logger.error(
                        f"Error: Received status code {response.status_code} - {response.text}"
                    )
                    self._login()

                time.sleep(1)

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")

    def _write_token(self, token, refresh_token):
        """
        Write tokens to temporary file.
        :param token:
        :param refresh_token:
        :return:
        """
        with open(self.token_temp_file_path, "w") as file:
            file.write(token)

        with open(self.refresh_token_temp_file_path, "w") as file:
            file.write(refresh_token)

    def _initialize_token_file(self):
        """
        Intialize token files
        :return:
        """
        try:
            with open(self.refresh_token_temp_file_path, "r") as file:
                file.read()
        except FileNotFoundError:
            with open(self.refresh_token_temp_file_path, "w") as file:
                file.write("")

        try:
            with open(self.token_temp_file_path, "r") as file:
                token = file.read()
                logger.debug(f"Token: {token}")
                if token != "":
                    self.headers["Authorization"] = f"Bearer {token}"

                self._request_challenge()
        except FileNotFoundError:
            with open(self.token_temp_file_path, "w") as file:
                file.write("")

    def _is_refresh_token_empty(self) -> bool:
        """
        Check if token is empty.
        :return: boolean
        """
        try:
            with open(os.path.join(self.refresh_token_temp_file_path), "r") as file:
                token = file.read()
                return token == ""
        except FileNotFoundError:
            return False

    def _request_challenge(self):
        """
        Check expired token by request to light API
        :return:
        """
        try:
            response = requests.get(
                "https://exodus.stockbit.com/research/indicator/new",
                headers=self.headers,
            )

            if response.status_code != 200:
                logger.error(
                    f"Error: Received status code {response.status_code} - {response.text}"
                )
                self._authenticate_stockbit()
            else:
                logger.info("Logged in successfully with existing token!")

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
