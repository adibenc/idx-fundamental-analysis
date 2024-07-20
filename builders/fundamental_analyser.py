from schemas.fundamental import Fundamental


class FundamentalAnalyser:
    def __init__(self, fundamentals: [Fundamental]):
        self.fundamentals = fundamentals

    def stocks_sheet(self) -> []:
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
        for fundamental in self.fundamentals:
            row = [
                fundamental.stock.ticker,
                fundamental.stock.name,
                fundamental.stock.ipo_date,
                fundamental.stock.market_cap,
                fundamental.stock.note,
                fundamental.stock.price,
                fundamental.stock.volume,
                fundamental.stock.change,
                fundamental.stock.percentage_change,
                fundamental.stock.average,
                fundamental.stock.close,
                fundamental.stock.high,
                fundamental.stock.low,
                fundamental.stock.open,
                fundamental.stock.ara,
                fundamental.stock.arb,
                fundamental.stock.frequency,
                fundamental.stock.fsell,
                fundamental.stock.fbuy,
            ]
            sheet_values.append(row)

        return sheet_values

    def key_statistics_sheet(self) -> []:
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

        for fundamental in self.fundamentals:
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

        return sheet_values

    def analysis_sheet(self) -> []:
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
        for fundamental in self.fundamentals:
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
