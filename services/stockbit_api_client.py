import os
import tempfile
import time

import requests

import hashlib
import json
from loguru import logger

from utils.logger_config import logger


class StockbitApiClient:
    """
    Handles HTTP requests to the Stockbit API, including authentication, retries, and file-based caching.
    """

    def __init__(self):
        """
        Initializes the StockbitHttpRequest with a URL and default headers.
        Authenticates with the Stockbit API upon initialization.
        Sets up file-based caching.
        """
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0",
        }
        self.is_authorise = False
        self.token_temp_file_path = os.path.join(
            tempfile.gettempdir(), "stockbit_token.tmp"
        )
        self.refresh_token_temp_file_path = os.path.join(
            tempfile.gettempdir(), "stockbit_refresh_token.tmp"
        )
        self._initialize_token_file()
        self.cache_dir = os.path.join("stockbit_cache")
        os.makedirs(self.cache_dir, exist_ok=True)  # Ensure cache directory exists

    def _get_cache_filename(self, url: str) -> str:
        """
        Generates a unique filename for caching based on the URL.  Uses a hash
        to avoid issues with long URLs or special characters.

        Args:
            url: The URL to be cached.

        Returns:
            The full path to the cache file.
        """
        hashed_url = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hashed_url}.json")

    def _load_cache(self, url: str) -> dict:
        """
        Loads cached data from a file, if it exists.

        Args:
            url: The URL corresponding to the data to load.

        Returns:
            The cached data as a dictionary, or None if not found or an error occurs.
        """
        cache_file = self._get_cache_filename(url)
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logger.error(f"Error loading cache from {cache_file}: {e}")
                return None
        return None

    def _save_cache(self, url: str, data: dict) -> None:
        """
        Saves data to a cache file.

        Args:
            url: The URL corresponding to the data being saved.
            data: The data to save (must be JSON serializable).
        """
        cache_file = self._get_cache_filename(url)
        try:
            with open(cache_file, "w") as f:
                json.dump(data, f)
        except (TypeError, OSError) as e:
            logger.error(f"Error saving cache to {cache_file}: {e}")

    def _request(self, url: str, method: str, payload: dict = None) -> dict:
        """
        Makes an HTTP request with the specified method and payload, retrying on failure,
        and uses file-based caching.

        Args:
            url: The URL to request.
            method: The HTTP method ("GET" or "POST").
            payload: Optional payload for POST requests.

        Returns:
            The JSON response from the server, or an empty dictionary on failure.
        """
        retry = 0
        while retry <= 3:
            try:
                cached_data = self._load_cache(url)
                if cached_data:
                    logger.debug(f"Loaded data from cache for {url}")
                    return cached_data

                if method == "GET":
                    response = requests.get(url, headers=self.headers)
                elif method == "POST":
                    response = requests.post(url, headers=self.headers, json=payload)
                else:
                    raise ValueError("Unsupported HTTP method")

                logger.debug(url)
                logger.debug(response.status_code)
                # avoid logging the entire response.json(), which can be very large
                if response.content:
                    logger.debug(f"Response snippet: {str(response.content[:64])}")

                if response.status_code == 200:
                    data = response.json()
                    self._save_cache(url, data)  # Cache the successful response
                    return data
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
                        break  # Don't retry for other errors

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e} retry: {retry}")
                break  # Don't retry on connection errors

            time.sleep(0.2)  # Consider increasing this backoff

        logger.error(f"Failed to retrieve data after retries for {url}")
        return {}  # Return an empty dict, consistent with original behavior

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
