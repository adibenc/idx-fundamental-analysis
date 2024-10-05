import os
import tempfile
import time

import requests

from utils.logger_config import logger


class StockbitHttpRequest:
    """
    Handles HTTP requests to the Stockbit API, including authentication and retries.

    Attributes:
    - url (str): The URL for the HTTP request.
    - headers (dict): Optional headers for the HTTP request.
    - token_temp_file_path (str): Path to a temporary file storing the authentication token.
    """

    def __init__(self, url: str, headers: dict = None):
        """
        Initializes the StockbitHttpRequest with a URL and optional headers.
        Authenticates with the Stockbit API upon initialization.

        Parameters:
        - url (str): The URL for the HTTP request.
        - headers (dict): Optional headers for the HTTP request.
        """
        self.url = url
        self.headers = headers
        self.token_temp_file_path = os.path.join(
            tempfile.gettempdir(), "stockbit-token.tmp"
        )

        self._authenticate_stockbit()

    def _request(self, method: str, payload: dict = None):
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
                    response = requests.get(self.url, headers=self.headers)
                elif method == "POST":
                    response = requests.post(
                        self.url, headers=self.headers, json=payload
                    )
                else:
                    raise ValueError("Unsupported HTTP method")

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

    def get(self):
        """
        Performs a GET request using the stored URL and headers.

        Returns:
        - dict: The JSON response from the server, or an empty dictionary on failure.
        """
        return self._request("GET")

    def post(self, payload: dict):
        """
        Performs a POST request using the stored URL, headers, and provided payload.

        Parameters:
        - payload (dict): The payload for the POST request.

        Returns:
        - dict: The JSON response from the server, or an empty dictionary on failure.
        """
        return self._request("POST", payload)

    def _authenticate_stockbit(self):
        """
        Authenticates with the Stockbit API and updates the authorization header.
        Stores the token in a temporary file for future use.
        """
        url = "https://stockbit.com/api/login/email"
        payload = {
            "username": os.getenv("STOCKBIT_USERNAME"),
            "password": os.getenv("STOCKBIT_PASSWORD"),
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)

            if response.status_code == 200:
                token = response.json()["data"]["access"]["token"]
                self.headers["Authorization"] = f"Bearer {token}"

                with open(self.token_temp_file_path, "w") as file:
                    file.write(token)

            else:
                logger.error(
                    f"Error: Received status code {response.status_code} - {response.text}"
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
