import json
import os

from dotenv import load_dotenv

from schemas.fundamental import Fundamental
from schemas.stock import Stock
from services.google_drive_service import GoogleDriveService
from utils.logger_config import logger

load_dotenv()


class Spreadsheet:
    """
    A class to manage the creation and data insertion of a Google Spreadsheet.

    Attributes:
        title (str): The title of the spreadsheet.
        google_drive_service (GoogleDriveService): An instance of GoogleDriveService to interact with Google Drive.
        spreadsheet_id (str): The ID of the created spreadsheet.
    """

    def __init__(self, title: str):
        """
        Initializes the Spreadsheet class with a title and creates a new spreadsheet.

        Args:
            title (str): The title of the spreadsheet.
        """
        self.title = title
        self.google_drive_service = GoogleDriveService()
        self.spreadsheet_id = ""
        self._create()

    def _create(self):
        """
        Creates a new spreadsheet and sets permissions for specified Google Drive emails.
        """
        self.spreadsheet_id = self.google_drive_service.create_spreadsheet(
            title=self.title
        )

        google_drive_emails = json.loads(os.getenv("GOOGLE_DRIVE_EMAILS"))
        for google_drive_email in google_drive_emails:
            self.google_drive_service.add_drive_permission(
                self.spreadsheet_id, google_drive_email
            )

    def insert_stock(self, stocks: [Stock]):
        """
        Inserts stock data into the spreadsheet.

        Args:
            stocks ([Stock]): A list of Stock objects to be inserted.
        """
        header = [
            "Ticker",
            "Name",
            "IPO Date",
            "Market Cap",
            "Note",
            "Price",
            "Volume",
            "Change",
            "Percentage Change",
            "Average",
            "Close Price",
            "High Price",
            "Open Price",
            "Low Price",
            "ARA Price",
            "ARB Price",
            "Frequency",
            "Frequency Sell",
            "Frequency Buy",
        ]
        sheet_values = [header]
        for stock in stocks:
            row = [
                stock.ticker,
                stock.name,
                stock.ipo_date,
                stock.market_cap,
                stock.note,
                stock.price,
                stock.volume,
                stock.change,
                stock.percentage_change,
                stock.average,
                stock.close,
                stock.high,
                stock.low,
                stock.open,
                stock.ara,
                stock.arb,
                stock.frequency,
                stock.fsell,
                stock.fbuy,
            ]
            sheet_values.append(row)

        self.google_drive_service.insert_data(
            self.spreadsheet_id, "idx-stocks", sheet_values
        )
        logger.info(
            f"Stocks has been inserted on https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"
        )

    def insert_fundamental(self, fundamentals: [Fundamental]):
        """
        Inserts fundamental data into the spreadsheet.

        Args:
            fundamentals ([Fundamental]): A list of Fundamental objects to be inserted.
        """
        header = [
            "Ticker",
            "Current PE Ratio (Annualised)",
            "Current PE Ratio (TTM)",
            "Forward PE Ratio",
            "IHSG PE Ratio TTM (Median)",
            "Earnings Yield (TTM)",
            "Current Price to Sales(TTM)",
            "Current Price to Book Value",
            "Current Price To Cashflow (TTM)",
            "Current Price To Free Cashflow (TTM)",
            "EV to EBIT (TTM)",
            "EV to EBITDA (TTM)",
            "PEG Ratio",
            "PEG Ratio (3yr)",
            "PEG (Forward)",
            "Current EPS (TTM)",
            "Current EPS (Annualised)",
            "Revenue Per Share (TTM)",
            "Cash Per Share (Quarter)",
            "Current Book Value Per Share",
            "Free Cashflow Per Share (TTM)",
            "Current Ratio (Quarter)",
            "Quick Ratio (Quarter)",
            "Debt to Equity Ratio (Quarter)",
            "LT Debt/Equity (Quarter)",
            "Total Liabilities/Equity (Quarter)",
            "Total Debt/Total Assets (Quarter)",
            "Financial Leverage (Quarter)",
            "Interest Coverage (TTM)",
            "Free cash flow (Quarter)",
            "Altman Z-Score (Modified)",
            "Return on Assets (TTM)",
            "Return on Equity (TTM)",
            "Return on Capital Employed (TTM)",
            "Return On Invested Capital (TTM)",
            "Days Sales Outstanding (Quarter)",
            "Days Inventory (Quarter)",
            "Days Payables Outstanding (Quarter)",
            "Cash Conversion Cycle (Quarter)",
            "Receivables Turnover (Quarter)",
            "Asset Turnover (TTM)",
            "Inventory Turnover (TTM)",
            "Gross Profit Margin (Quarter)",
            "Operating Profit Margin (Quarter)",
            "Net Profit Margin (Quarter)",
            "Revenue (Quarter YoY Growth)",
            "Gross Profit (Quarter YoY Growth)",
            "Net Income (Quarter YoY Growth)",
            "Dividend",
            "Dividend (TTM)",
            "Payout Ratio",
            "Dividend Yield",
            "Latest Dividend Ex-Date",
            "Piotroski F-Score",
            "EPS Rating",
            "Relative Strength Rating",
            "Rank (Market Cap)",
            "Rank (Current PE Ratio TTM)",
            "Rank (Earnings Yield)",
            "Rank (P/S)",
            "Rank (P/B)",
            "Rank (Near 52 Weeks High)",
            "Revenue (TTM)",
            "Gross Profit (TTM)",
            "EBITDA (TTM)",
            "Net Income (TTM)",
            "Cash (Quarter)",
            "Total Assets (Quarter)",
            "Total Liabilities (Quarter)",
            "Working Capital (Quarter)",
            "Total Equity",
            "Long-term Debt (Quarter)",
            "Short-term Debt (Quarter)",
            "Total Debt (Quarter)",
            "Net Debt (Quarter)",
            "Cash From Operations (TTM)",
            "Cash From Investing (TTM)",
            "Cash From Financing (TTM)",
            "Capital expenditure (TTM)",
            "Free cash flow (TTM)",
            "1 Week Price Returns",
            "3 Month Price Returns",
            "1 Month Price Returns",
            "6 Month Price Returns",
            "1 Year Price Returns",
            "3 Year Price Returns",
            "5 Year Price Returns",
            "10 Year Price Returns",
            "Year to Date Price Returns",
            "52 Week High",
            "52 Week Low",
            "Market Cap",
            "Enterprise Value",
            "Current Share Outstanding",
        ]
        sheet_values = [header]

        for fundamental in fundamentals:
            row = [
                fundamental.stock.ticker,
                fundamental.current_valuation.current_pe_ratio_annual,
                fundamental.current_valuation.current_pe_ratio_ttm,
                fundamental.current_valuation.forward_pe_ratio,
                fundamental.current_valuation.ihsg_pe_ratio_ttm_median,
                fundamental.current_valuation.earnings_yield_ttm,
                fundamental.current_valuation.current_price_to_sales_ttm,
                fundamental.current_valuation.current_price_to_book_value,
                fundamental.current_valuation.current_price_to_cashflow_ttm,
                fundamental.current_valuation.current_price_to_free_cashflow_ttm,
                fundamental.current_valuation.ev_to_ebit_ttm,
                fundamental.current_valuation.ev_to_ebitda_ttm,
                fundamental.current_valuation.peg_ratio,
                fundamental.current_valuation.peg_ratio_3yr,
                fundamental.current_valuation.peg_forward,
                fundamental.per_share.current_eps_ttm,
                fundamental.per_share.current_eps_annualised,
                fundamental.per_share.revenue_per_share_ttm,
                fundamental.per_share.cash_per_share_quarter,
                fundamental.per_share.current_book_value_per_share,
                fundamental.per_share.free_cashflow_per_share_ttm,
                fundamental.solvency.current_ratio_quarter,
                fundamental.solvency.quick_ratio_quarter,
                fundamental.solvency.debt_to_equity_ratio_quarter,
                fundamental.solvency.lt_debt_equity_quarter,
                fundamental.solvency.total_liabilities_equity_quarter,
                fundamental.solvency.total_debt_total_assets_quarter,
                fundamental.solvency.financial_leverage_quarter,
                fundamental.solvency.interest_rate_coverage_ttm,
                fundamental.solvency.free_cash_flow_quarter,
                fundamental.solvency.altman_z_score_modified,
                fundamental.management_effectiveness.return_on_assets_ttm,
                fundamental.management_effectiveness.return_on_equity_ttm,
                fundamental.management_effectiveness.return_on_capital_employed_ttm,
                fundamental.management_effectiveness.return_on_invested_capital_ttm,
                fundamental.management_effectiveness.days_sales_outstanding_quarter,
                fundamental.management_effectiveness.days_inventory_quarter,
                fundamental.management_effectiveness.days_payables_outstanding_quarter,
                fundamental.management_effectiveness.cash_conversion_cycle_quarter,
                fundamental.management_effectiveness.receivables_turnover_quarter,
                fundamental.management_effectiveness.asset_turnover_ttm,
                fundamental.management_effectiveness.inventory_turnover_ttm,
                fundamental.profitability.gross_profit_margin_quarter,
                fundamental.profitability.operating_profit_margin_quarter,
                fundamental.profitability.net_profit_margin_quarter,
                fundamental.growth.revenue_quarter_yoy_growth,
                fundamental.growth.gross_profit_quarter_yoy_growth,
                fundamental.growth.net_income_quarter_yoy_growth,
                fundamental.dividend.dividend,
                fundamental.dividend.dividend_ttm,
                fundamental.dividend.payout_ratio,
                fundamental.dividend.dividend_yield,
                fundamental.dividend.latest_dividend_ex_date,
                fundamental.market_rank.piotroski_f_score,
                fundamental.market_rank.eps_rating,
                fundamental.market_rank.relative_strength_rating,
                fundamental.market_rank.rank_market_cap,
                fundamental.market_rank.rank_current_pe_ratio_ttm,
                fundamental.market_rank.rank_earnings_yield,
                fundamental.market_rank.rank_p_s,
                fundamental.market_rank.rank_p_b,
                fundamental.market_rank.rank_near_52_weeks_high,
                fundamental.income_statement.revenue_ttm,
                fundamental.income_statement.gross_profit_ttm,
                fundamental.income_statement.ebitda_ttm,
                fundamental.income_statement.net_income_ttm,
                fundamental.balance_sheet.cash_quarter,
                fundamental.balance_sheet.total_assets_quarter,
                fundamental.balance_sheet.total_liabilities_quarter,
                fundamental.balance_sheet.working_capital_quarter,
                fundamental.balance_sheet.total_equity,
                fundamental.balance_sheet.long_term_debt_quarter,
                fundamental.balance_sheet.short_term_debt_quarter,
                fundamental.balance_sheet.total_debt_quarter,
                fundamental.balance_sheet.net_debt_quarter,
                fundamental.cash_flow_statement.cash_from_operations_ttm,
                fundamental.cash_flow_statement.cash_from_investing_ttm,
                fundamental.cash_flow_statement.cash_from_financing_ttm,
                fundamental.cash_flow_statement.capital_expenditure_ttm,
                fundamental.cash_flow_statement.free_cash_flow_ttm,
                fundamental.price_performance.one_week_price_returns,
                fundamental.price_performance.three_month_price_returns,
                fundamental.price_performance.one_month_price_returns,
                fundamental.price_performance.six_month_price_returns,
                fundamental.price_performance.one_year_price_returns,
                fundamental.price_performance.three_year_price_returns,
                fundamental.price_performance.five_year_price_returns,
                fundamental.price_performance.ten_year_price_returns,
                fundamental.price_performance.year_to_date_price_returns,
                fundamental.price_performance.fifty_two_week_high,
                fundamental.price_performance.fifty_two_week_low,
                fundamental.stats.market_cap,
                fundamental.stats.enterprise_value,
                fundamental.stats.current_share_outstanding,
            ]
            sheet_values.append(row)

        self.google_drive_service.insert_data(
            self.spreadsheet_id, "fundamentals", sheet_values
        )
        logger.info(
            f"Fundamentals has been inserted on https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"
        )

    def insert_analysis(self, fundamentals: [Fundamental]):
        """
        Inserts fundamental analysis data into the spreadsheet.

        Args:
            fundamentals ([Fundamental]): A list of Fundamental objects to be inserted.
        """

        headers = ["Ticker", "PBV x ROE", "Close Price", "Price to Equity Discount (%)"]

        sheet_values = [headers]
        for fundamental in fundamentals:
            normal_price = (
                fundamental.per_share.current_book_value_per_share
                * fundamental.management_effectiveness.return_on_equity_ttm
                * 10
            )

            if normal_price > 0:
                price_to_equity_disct = 1 - (
                    (fundamental.stock.close / normal_price) * 100
                )
            else:
                price_to_equity_disct = 0

            row = [
                fundamental.stock.ticker,
                round(normal_price, 2),
                fundamental.stock.close,
                round(price_to_equity_disct, 2),
            ]

            sheet_values.append(row)

        self.google_drive_service.insert_data(
            self.spreadsheet_id, "analyses", sheet_values
        )

        logger.info(
            f"Analysis has been inserted on https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"
        )
