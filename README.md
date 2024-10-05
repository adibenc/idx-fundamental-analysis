# IDX Fundamental Analysis

## Description

IDX Fundamental Analysis project aims to retrieve and analyse fundamental stock data of companies listed on the Indonesian
Stock Exchange (IDX). It fetches stock data and key statistics using Selenium, requests, and various provider APIs, and
stores the resultant data in Google Sheets or local Excel file for easy access and analysis.

## Features

- **Fetch Stock Data from IDX**: Use Selenium web driver to scrape stock data from IDX.
- **Retrieve Fundamental Data**: Obtain key statistics and fundamental data using StockBit and YFinance API.
- **Google Sheets Integration**: Create and update Google Sheets with stock data using Google Drive API. Required
  Google Service Account environment variable.
- **Save as Excel**: Stored the fundamental analysis data in your local file.
- **Logging**: Robust logging using Loguru for debugging and tracking purposes.

## Installation

### Prerequisites

- Python 3.12
- [Poetry](https://python-poetry.org/docs/#installation)

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/idx-fundamental.git
    cd idx-fundamental
    ```

2. Install dependencies:

    ```bash
    poetry install --no-root
    ```

3. Set up environment variables:

   Create a `.env` file in the project root directory and add the following environment variables:

    ```env
    GOOGLE_SERVICE_ACCOUNT='{
      "type": "service_account",
      "project_id": "...",
      "private_key_id": "...",
      "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
      "client_email": "...",
      "client_id": "...",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "..."
    }'
  
    GOOGLE_DRIVE_EMAILS='["email1@gmail.com", "email2@gmail.com"]'
    STOCKBIT_USERNAME='hello@example.com'
    STOCKBIT_PASSWORD='pwd'
    ```

## Usage

1. Run the main script:

    ```bash
    python main.py -f -o excel
    ```
    - The `-f` or `--full-retrieve` argument is optional. If included, the script will retrieve full stock data from
      IDX.
      If not set, it only retrieve first page which is only 10 stocks.

    - The `-o` or `--output-format` argument with two choices: `spreadsheet` and `excel`. Output will be saved into
      Google
      Sheet or Excel local file.
    - This will start the process of fetching stock data from IDX, retrieving key statistics from StockBit, and
      inserting them into a Google Sheet.

## Configuration

The primary configuration options include environment variables set in the `.env` file. Ensure you have authenticated
and authorized access to Google Drive and possessed a valid username and password for StockBit API access.

## Contribution Guidelines

Contributions are welcome! Feel free to open issues or submit pull requests. Please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Make your changes, ensuring tests pass.
4. Open a pull request with a detailed description of your changes.

## Testing

Currently, the project does not include unit tests. However, testing can be done by running the `main.py` script and
verifying the output in the Google Sheet.

## Result

### Screenshot
- [IDX Fundamental Analysis 05-10-2024](https://drive.zeroinside.id/s/sJ655E5gSSRGad8)

### Screencast
![demo-idx-fundamental](https://github.com/user-attachments/assets/15a56238-e924-4100-8bb3-2c65a5c5e5ea)

## TODO

1. Stored data to SQLlite database.
2. Dashboard support using Streamlit.
3. Sentiment Analysis using LLMs, will use OpenAI and Ollama.
4. Time Series Forecasting using ETS, ARIMA, and Prophet.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Stockbit](https://stockbit.com) for IDX composite key statistics and stock prices data.
- [Selenium](https://www.selenium.dev/) for web scraping capabilities.
- [Loguru](https://github.com/Delgan/loguru) for logging.
- [yfinance](https://github.com/ranaroussi/yfinance) for financial data.
- [Google APIs](https://developers.google.com/api-client-library/python/) for integration with Google Sheets.
