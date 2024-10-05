from schemas.stock import Stock


class FundamentalAnalyser:
    """
    Analyzes fundamental data for a list of stocks and generates various sheets.

    Attributes:
    - stocks (list of Stock): A list of Stock objects to be analyzed.
    """

    def __init__(self, stocks: [Stock]):
        """
        Initializes the FundamentalAnalyser with a list of stocks.

        Parameters:
        - stocks (list of Stock): A list of Stock objects containing fundamental data.
        """
        self.stocks = stocks

    def stocks_sheet(self) -> []:
        """
        Generates a sheet of basic stock information.

        Returns:
        - list of list: A list of rows, each containing basic stock information.
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
        for stock in self.stocks:
            row = [
                stock.fundamental.stock.ticker,
                stock.fundamental.stock.name,
                stock.fundamental.stock.ipo_date,
                stock.fundamental.stock.market_cap,
                stock.fundamental.stock.note,
                stock.fundamental.stock.price,
                stock.fundamental.stock.volume,
                stock.fundamental.stock.change,
                stock.fundamental.stock.percentage_change,
                stock.fundamental.stock.average,
                stock.fundamental.stock.close,
                stock.fundamental.stock.high,
                stock.fundamental.stock.low,
                stock.fundamental.stock.open,
                stock.fundamental.stock.ara,
                stock.fundamental.stock.arb,
                stock.fundamental.stock.frequency,
                stock.fundamental.stock.fsell,
                stock.fundamental.stock.fbuy,
            ]
            sheet_values.append(row)

        return sheet_values

    def key_statistics_sheet(self) -> []:
        """
        Generates a sheet of key statistics for each stock.

        Returns:
        - list of list: A list of rows, each containing key statistics for a stock.
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

        for stock in self.stocks:
            row = [
                stock.fundamental.stock.ticker,
                stock.fundamental.current_valuation.current_pe_ratio_annual,
                stock.fundamental.current_valuation.current_pe_ratio_ttm,
                stock.fundamental.current_valuation.forward_pe_ratio,
                stock.fundamental.current_valuation.ihsg_pe_ratio_ttm_median,
                stock.fundamental.current_valuation.earnings_yield_ttm,
                stock.fundamental.current_valuation.current_price_to_sales_ttm,
                stock.fundamental.current_valuation.current_price_to_book_value,
                stock.fundamental.current_valuation.current_price_to_cashflow_ttm,
                stock.fundamental.current_valuation.current_price_to_free_cashflow_ttm,
                stock.fundamental.current_valuation.ev_to_ebit_ttm,
                stock.fundamental.current_valuation.ev_to_ebitda_ttm,
                stock.fundamental.current_valuation.peg_ratio,
                stock.fundamental.current_valuation.peg_ratio_3yr,
                stock.fundamental.current_valuation.peg_forward,
                stock.fundamental.per_share.current_eps_ttm,
                stock.fundamental.per_share.current_eps_annualised,
                stock.fundamental.per_share.revenue_per_share_ttm,
                stock.fundamental.per_share.cash_per_share_quarter,
                stock.fundamental.per_share.current_book_value_per_share,
                stock.fundamental.per_share.free_cashflow_per_share_ttm,
                stock.fundamental.solvency.current_ratio_quarter,
                stock.fundamental.solvency.quick_ratio_quarter,
                stock.fundamental.solvency.debt_to_equity_ratio_quarter,
                stock.fundamental.solvency.lt_debt_equity_quarter,
                stock.fundamental.solvency.total_liabilities_equity_quarter,
                stock.fundamental.solvency.total_debt_total_assets_quarter,
                stock.fundamental.solvency.financial_leverage_quarter,
                stock.fundamental.solvency.interest_rate_coverage_ttm,
                stock.fundamental.solvency.free_cash_flow_quarter,
                stock.fundamental.solvency.altman_z_score_modified,
                stock.fundamental.management_effectiveness.return_on_assets_ttm,
                stock.fundamental.management_effectiveness.return_on_equity_ttm,
                stock.fundamental.management_effectiveness.return_on_capital_employed_ttm,
                stock.fundamental.management_effectiveness.return_on_invested_capital_ttm,
                stock.fundamental.management_effectiveness.days_sales_outstanding_quarter,
                stock.fundamental.management_effectiveness.days_inventory_quarter,
                stock.fundamental.management_effectiveness.days_payables_outstanding_quarter,
                stock.fundamental.management_effectiveness.cash_conversion_cycle_quarter,
                stock.fundamental.management_effectiveness.receivables_turnover_quarter,
                stock.fundamental.management_effectiveness.asset_turnover_ttm,
                stock.fundamental.management_effectiveness.inventory_turnover_ttm,
                stock.fundamental.profitability.gross_profit_margin_quarter,
                stock.fundamental.profitability.operating_profit_margin_quarter,
                stock.fundamental.profitability.net_profit_margin_quarter,
                stock.fundamental.growth.revenue_quarter_yoy_growth,
                stock.fundamental.growth.gross_profit_quarter_yoy_growth,
                stock.fundamental.growth.net_income_quarter_yoy_growth,
                stock.fundamental.dividend.dividend,
                stock.fundamental.dividend.dividend_ttm,
                stock.fundamental.dividend.payout_ratio,
                stock.fundamental.dividend.dividend_yield,
                stock.fundamental.dividend.latest_dividend_ex_date,
                stock.fundamental.market_rank.piotroski_f_score,
                stock.fundamental.market_rank.eps_rating,
                stock.fundamental.market_rank.relative_strength_rating,
                stock.fundamental.market_rank.rank_market_cap,
                stock.fundamental.market_rank.rank_current_pe_ratio_ttm,
                stock.fundamental.market_rank.rank_earnings_yield,
                stock.fundamental.market_rank.rank_p_s,
                stock.fundamental.market_rank.rank_p_b,
                stock.fundamental.market_rank.rank_near_52_weeks_high,
                stock.fundamental.income_statement.revenue_ttm,
                stock.fundamental.income_statement.gross_profit_ttm,
                stock.fundamental.income_statement.ebitda_ttm,
                stock.fundamental.income_statement.net_income_ttm,
                stock.fundamental.balance_sheet.cash_quarter,
                stock.fundamental.balance_sheet.total_assets_quarter,
                stock.fundamental.balance_sheet.total_liabilities_quarter,
                stock.fundamental.balance_sheet.working_capital_quarter,
                stock.fundamental.balance_sheet.total_equity,
                stock.fundamental.balance_sheet.long_term_debt_quarter,
                stock.fundamental.balance_sheet.short_term_debt_quarter,
                stock.fundamental.balance_sheet.total_debt_quarter,
                stock.fundamental.balance_sheet.net_debt_quarter,
                stock.fundamental.cash_flow_statement.cash_from_operations_ttm,
                stock.fundamental.cash_flow_statement.cash_from_investing_ttm,
                stock.fundamental.cash_flow_statement.cash_from_financing_ttm,
                stock.fundamental.cash_flow_statement.capital_expenditure_ttm,
                stock.fundamental.cash_flow_statement.free_cash_flow_ttm,
                stock.fundamental.price_performance.one_week_price_returns,
                stock.fundamental.price_performance.three_month_price_returns,
                stock.fundamental.price_performance.one_month_price_returns,
                stock.fundamental.price_performance.six_month_price_returns,
                stock.fundamental.price_performance.one_year_price_returns,
                stock.fundamental.price_performance.three_year_price_returns,
                stock.fundamental.price_performance.five_year_price_returns,
                stock.fundamental.price_performance.ten_year_price_returns,
                stock.fundamental.price_performance.year_to_date_price_returns,
                stock.fundamental.price_performance.fifty_two_week_high,
                stock.fundamental.price_performance.fifty_two_week_low,
                stock.fundamental.stats.market_cap,
                stock.fundamental.stats.enterprise_value,
                stock.fundamental.stats.current_share_outstanding,
            ]
            sheet_values.append(row)

        return sheet_values

    def analysis_sheet(self) -> []:
        """
        Generates a sheet of analysis for each stock that derives from fundamental.

        Returns:
        - list of list: A list of rows, each containing key statistics for a stock.
        """
        headers = [
            "Ticker",
            "PBV x ROE",
            "Close Price",
            "Price to Equity Discount (%)",
            "Relative PE ratio (TTM)",
            "EPS Growth",
            "Debt to Total Assets Ratio",
            "Liquidity Differential",
            "CCE",
            "Operating Efficiency",
            "Dividend Payout Efficiency",
            "Yearly Price Change",
            "Composite Rank",
            "Net Debt to Equity",
        ]

        sheet_values = [headers]
        for stock in self.stocks:
            fundamental = stock.fundamental

            normal_price = (
                fundamental.per_share.current_book_value_per_share
                * fundamental.management_effectiveness.return_on_equity_ttm
                * 10
            )

            if normal_price > 0:
                price_to_equity_disct = abs(
                    1 - (fundamental.stock.close / normal_price) * 100
                )
            else:
                price_to_equity_disct = 0

            if fundamental.current_valuation.ihsg_pe_ratio_ttm_median > 0:
                relative_pe_ratio_ttm = (
                    fundamental.market_rank.rank_current_pe_ratio_ttm
                    / fundamental.current_valuation.ihsg_pe_ratio_ttm_median
                )
            else:
                relative_pe_ratio_ttm = 0

            if fundamental.per_share.current_eps_ttm > 0:
                eps_growth = (
                    fundamental.per_share.current_eps_annualised
                    - fundamental.per_share.current_eps_ttm
                ) / fundamental.per_share.current_eps_ttm
            else:
                eps_growth = 0

            if fundamental.balance_sheet.total_assets_quarter > 0:
                debt_to_total_assets_ratio = (
                    fundamental.balance_sheet.total_debt_quarter
                    / fundamental.balance_sheet.total_assets_quarter
                )
            else:
                debt_to_total_assets_ratio = 0

            if fundamental.solvency.quick_ratio_quarter > 0:
                liquidity_differential = (
                    fundamental.solvency.current_ratio_quarter
                    / fundamental.solvency.quick_ratio_quarter
                )
            else:
                liquidity_differential = 0

            if fundamental.income_statement.revenue_ttm > 0:
                cce = (
                    fundamental.cash_flow_statement.cash_from_operations_ttm
                    / fundamental.income_statement.revenue_ttm
                )
            else:
                cce = 0

            if fundamental.profitability.gross_profit_margin_quarter > 0:
                operating_efficiency = (
                    fundamental.profitability.operating_profit_margin_quarter
                    / fundamental.profitability.gross_profit_margin_quarter
                )
            else:
                operating_efficiency = 0

            if fundamental.income_statement.net_income_ttm > 0:
                dividend_payout_efficiency = (
                    fundamental.dividend.dividend + fundamental.dividend.dividend_ttm
                ) / (2 * fundamental.income_statement.net_income_ttm)
            else:
                dividend_payout_efficiency = 0

            if fundamental.income_statement.revenue_ttm > 0:
                yearly_price_change = (
                    fundamental.price_performance.one_year_price_returns
                    / fundamental.income_statement.revenue_ttm
                )
            else:
                yearly_price_change = 0

            composite_rank = (
                fundamental.market_rank.rank_current_pe_ratio_ttm
                + fundamental.market_rank.rank_current_pe_ratio_ttm
                + fundamental.market_rank.rank_earnings_yield
                + fundamental.market_rank.rank_p_s
                + fundamental.market_rank.rank_p_b
                + fundamental.market_rank.rank_near_52_weeks_high
            ) / 6

            if fundamental.balance_sheet.total_equity > 0:
                net_debt_to_equity = (
                    fundamental.balance_sheet.net_debt_quarter
                    / fundamental.balance_sheet.total_equity
                )
            else:
                net_debt_to_equity = 0

            row = [
                fundamental.stock.ticker,
                round(normal_price, 2),
                fundamental.stock.close,
                round(price_to_equity_disct, 2),
                round(relative_pe_ratio_ttm, 2),
                round(eps_growth, 2),
                round(debt_to_total_assets_ratio, 2),
                round(liquidity_differential, 2),
                round(cce, 2),
                round(operating_efficiency, 2),
                round(dividend_payout_efficiency, 2),
                round(yearly_price_change, 2),
                round(composite_rank, 2),
                round(net_debt_to_equity, 2),
            ]

            sheet_values.append(row)

        return sheet_values
