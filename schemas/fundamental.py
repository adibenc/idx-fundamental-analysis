from dataclasses import dataclass

from schemas.stock import Stock


@dataclass
class CurrentValuation:
    current_pe_ratio_annual: float = 0.0
    current_pe_ratio_ttm: float = 0.0
    forward_pe_ratio: float = 0.0
    ihsg_pe_ratio_ttm_median: float = 0.0
    earnings_yield_ttm: float = 0.0
    current_price_to_sales_ttm: float = 0.0
    current_price_to_book_value: float = 0.0
    current_price_to_cashflow_ttm: float = 0.0
    current_price_to_free_cashflow_ttm: float = 0.0
    ev_to_ebit_ttm: float = 0.0
    ev_to_ebitda_ttm: float = 0.0
    peg_ratio: float = 0.0
    peg_ratio_3yr: float = 0.0
    peg_forward: float = 0.0


@dataclass
class PerShare:
    current_eps_ttm: float = 0
    current_eps_annualised: float = 0
    revenue_per_share_ttm: float = 0
    cash_per_share_quarter: float = 0
    current_book_value_per_share: float = 0
    free_cashflow_per_share_ttm: float = 0


@dataclass
class Solvency:
    current_ratio_quarter: float = 0
    quick_ratio_quarter: float = 0
    debt_to_equity_ratio_quarter: float = 0
    lt_debt_equity_quarter: float = 0
    total_liabilities_equity_quarter: float = 0
    total_debt_total_assets_quarter: float = 0
    financial_leverage_quarter: float = 0
    interest_rate_coverage_ttm: float = 0
    free_cash_flow_quarter: float = 0
    altman_z_score_modified: float = 0


@dataclass
class ManagementEffectiveness:
    return_on_assets_ttm: float = 0
    return_on_equity_ttm: float = 0
    return_on_capital_employed_ttm: float = 0
    return_on_invested_capital_ttm: float = 0
    days_sales_outstanding_quarter: float = 0
    days_inventory_quarter: float = 0
    days_payables_outstanding_quarter: float = 0
    cash_conversion_cycle_quarter: float = 0
    receivables_turnover_quarter: float = 0
    asset_turnover_ttm: float = 0
    inventory_turnover_ttm: float = 0


@dataclass
class Profitability:
    gross_profit_margin_quarter: float = 0.0
    operating_profit_margin_quarter: float = 0.0
    net_profit_margin_quarter: float = 0.0


@dataclass
class Growth:
    revenue_quarter_yoy_growth: float = 0.0
    gross_profit_quarter_yoy_growth: float = 0.0
    net_income_quarter_yoy_growth: float = 0.0


@dataclass
class Dividend:
    dividend: float = 0.0
    dividend_ttm: float = 0.0
    payout_ratio: float = 0.0
    dividend_yield: float = 0.0
    latest_dividend_ex_date: str = ""


@dataclass
class MarketRank:
    piotroski_f_score: float = 0.0
    eps_rating: float = 0.0
    relative_strength_rating: float = 0.0
    rank_market_cap: float = 0.0
    rank_current_pe_ratio_ttm: float = 0.0
    rank_earnings_yield: float = 0.0
    rank_p_s: float = 0.0
    rank_p_b: float = 0.0
    rank_near_52_weeks_high: float = 0.0


@dataclass
class IncomeStatement:
    revenue_ttm: float = 0.0
    gross_profit_ttm: float = 0.0
    ebitda_ttm: float = 0.0
    net_income_ttm: float = 0.0


@dataclass
class BalanceSheet:
    cash_quarter: float = 0.0
    total_assets_quarter: float = 0.0
    total_liabilities_quarter: float = 0.0
    working_capital_quarter: float = 0.0
    total_equity: float = 0.0
    long_term_debt_quarter: float = 0.0
    short_term_debt_quarter: float = 0.0
    total_debt_quarter: float = 0.0
    net_debt_quarter: float = 0.0


@dataclass
class CashFlowStatement:
    cash_from_operations_ttm: float = 0.0
    cash_from_investing_ttm: float = 0.0
    cash_from_financing_ttm: float = 0.0
    capital_expenditure_ttm: float = 0.0
    free_cash_flow_ttm: float = 0.0


@dataclass
class PricePerformance:
    one_week_price_returns: float = 0.0
    three_month_price_returns: float = 0.0
    one_month_price_returns: float = 0.0
    six_month_price_returns: float = 0.0
    one_year_price_returns: float = 0.0
    three_year_price_returns: float = 0.0
    five_year_price_returns: float = 0.0
    ten_year_price_returns: float = 0.0
    year_to_date_price_returns: float = 0.0
    fifty_two_week_high: float = 0.0
    fifty_two_week_low: float = 0.0


@dataclass
class Stats:
    current_share_outstanding: float = 0.0
    market_cap: float = 0.0
    enterprise_value: float = 0.0


@dataclass
class Fundamental:
    stock: Stock = Stock
    stats: Stats = Stats
    current_valuation: CurrentValuation = CurrentValuation
    per_share: PerShare = PerShare
    solvency: Solvency = Solvency
    management_effectiveness: ManagementEffectiveness = ManagementEffectiveness
    profitability: Profitability = Profitability
    growth: Growth = Growth
    dividend: Dividend = Dividend
    market_rank: MarketRank = MarketRank
    income_statement: IncomeStatement = IncomeStatement
    balance_sheet: BalanceSheet = BalanceSheet
    cash_flow_statement: CashFlowStatement = CashFlowStatement
    price_performance: PricePerformance = PricePerformance
