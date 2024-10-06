from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import Relationship

from db.models import BaseModel


class Fundamental(BaseModel):
    __tablename__ = "fundamentals"

    stats_id = Column(Integer, ForeignKey("stats.id"))
    current_valuation_id = Column(Integer, ForeignKey("current_valuations.id"))
    per_share_id = Column(Integer, ForeignKey("per_shares.id"))
    solvency_id = Column(Integer, ForeignKey("solvencies.id"))
    management_effectiveness_id = Column(
        Integer, ForeignKey("management_effectivenesses.id")
    )
    profitability_id = Column(Integer, ForeignKey("profitabilities.id"))
    growth_id = Column(Integer, ForeignKey("growths.id"))
    dividend_id = Column(Integer, ForeignKey("dividends.id"))
    market_rank_id = Column(Integer, ForeignKey("market_ranks.id"))
    income_statement_id = Column(Integer, ForeignKey("income_statements.id"))
    balance_sheet_id = Column(Integer, ForeignKey("balance_sheets.id"))
    cash_flow_statement_id = Column(Integer, ForeignKey("cash_flow_statements.id"))
    price_performance_id = Column(Integer, ForeignKey("price_performances.id"))

    stock_ticker = Column(String, ForeignKey("stocks.ticker"))


class CurrentValuation(BaseModel):
    __tablename__ = "current_valuations"
    id = Column(Integer, primary_key=True)
    current_pe_ratio_annual = Column(Float, default=0.0)
    current_pe_ratio_ttm = Column(Float, default=0.0)
    forward_pe_ratio = Column(Float, default=0.0)
    ihsg_pe_ratio_ttm_median = Column(Float, default=0.0)
    earnings_yield_ttm = Column(Float, default=0.0)
    current_price_to_sales_ttm = Column(Float, default=0.0)
    current_price_to_book_value = Column(Float, default=0.0)
    current_price_to_cashflow_ttm = Column(Float, default=0.0)
    current_price_to_free_cashflow_ttm = Column(Float, default=0.0)
    ev_to_ebit_ttm = Column(Float, default=0.0)
    ev_to_ebitda_ttm = Column(Float, default=0.0)
    peg_ratio = Column(Float, default=0.0)
    peg_ratio_3yr = Column(Float, default=0.0)
    peg_forward = Column(Float, default=0.0)
    fundamental = Relationship("Fundamental", backref="current_valuation")


class PerShare(BaseModel):
    __tablename__ = "per_shares"
    id = Column(Integer, primary_key=True)
    current_eps_ttm = Column(Float, default=0.0)
    current_eps_annualised = Column(Float, default=0.0)
    revenue_per_share_ttm = Column(Float, default=0.0)
    cash_per_share_quarter = Column(Float, default=0.0)
    current_book_value_per_share = Column(Float, default=0.0)
    free_cashflow_per_share_ttm = Column(Float, default=0.0)
    fundamental = Relationship("Fundamental", backref="per_share")


class Solvency(BaseModel):
    __tablename__ = "solvencies"
    id = Column(Integer, primary_key=True)
    current_ratio_quarter = Column(Float, default=0.0)
    quick_ratio_quarter = Column(Float, default=0.0)
    debt_to_equity_ratio_quarter = Column(Float, default=0.0)
    lt_debt_equity_quarter = Column(Float, default=0.0)
    total_liabilities_equity_quarter = Column(Float, default=0.0)
    total_debt_total_assets_quarter = Column(Float, default=0.0)
    financial_leverage_quarter = Column(Float, default=0.0)
    interest_rate_coverage_ttm = Column(Float, default=0.0)
    free_cash_flow_quarter = Column(Float, default=0.0)
    altman_z_score_modified = Column(Float, default=0.0)
    fundamental = Relationship("Fundamental", backref="solvency")


class ManagementEffectiveness(BaseModel):
    __tablename__ = "management_effectivenesses"
    id = Column(Integer, primary_key=True)
    return_on_assets_ttm = Column(Float, default=0.0)
    return_on_equity_ttm = Column(Float, default=0.0)
    return_on_capital_employed_ttm = Column(Float, default=0.0)
    return_on_invested_capital_ttm = Column(Float, default=0.0)
    days_sales_outstanding_quarter = Column(Float, default=0.0)
    days_inventory_quarter = Column(Float, default=0.0)
    days_payables_outstanding_quarter = Column(Float, default=0.0)
    cash_conversion_cycle_quarter = Column(Float, default=0.0)
    receivables_turnover_quarter = Column(Float, default=0.0)
    asset_turnover_ttm = Column(Float, default=0.0)
    inventory_turnover_ttm = Column(Float, default=0.0)
    fundamental = Relationship("Fundamental", backref="management_effectiveness")


class Profitability(BaseModel):
    __tablename__ = "profitabilities"
    id = Column(Integer, primary_key=True)
    gross_profit_margin_quarter = Column(Float, default=0.0)
    operating_profit_margin_quarter = Column(Float, default=0.0)
    net_profit_margin_quarter = Column(Float, default=0.0)
    fundamental = Relationship("Fundamental", backref="profitability")


class Growth(BaseModel):
    __tablename__ = "growths"
    id = Column(Integer, primary_key=True)
    revenue_quarter_yoy_growth = Column(Float, default=0.0)
    gross_profit_quarter_yoy_growth = Column(Float, default=0.0)
    net_income_quarter_yoy_growth = Column(Float, default=0.0)
    fundamental = Relationship("Fundamental", backref="growth")


class Dividend(BaseModel):
    __tablename__ = "dividends"
    id = Column(Integer, primary_key=True)
    dividend = Column(Float, default=0.0)
    dividend_ttm = Column(Float, default=0.0)
    payout_ratio = Column(Float, default=0.0)
    dividend_yield = Column(Float, default=0.0)
    latest_dividend_ex_date = Column(String, default="")
    fundamental = Relationship("Fundamental", backref="dividend")


class MarketRank(BaseModel):
    __tablename__ = "market_ranks"
    id = Column(Integer, primary_key=True)
    piotroski_f_score = Column(Float, default=0.0)
    eps_rating = Column(Float, default=0.0)
    relative_strength_rating = Column(Float, default=0.0)
    rank_market_cap = Column(Float, default=0.0)
    rank_current_pe_ratio_ttm = Column(Float, default=0.0)
    rank_earnings_yield = Column(Float, default=0.0)
    rank_p_s = Column(Float, default=0.0)
    rank_p_b = Column(Float, default=0.0)
    rank_near_52_weeks_high = Column(Float, default=0.0)
    fundamental = Relationship("Fundamental", backref="market_rank")


class IncomeStatement(BaseModel):
    __tablename__ = "income_statements"
    id = Column(Integer, primary_key=True)
    revenue_ttm = Column(Float, default=0.0)
    gross_profit_ttm = Column(Float, default=0.0)
    ebitda_ttm = Column(Float, default=0.0)
    net_income_ttm = Column(Float, default=0.0)
    fundamental = Relationship("Fundamental", backref="income_statement")


class BalanceSheet(BaseModel):
    __tablename__ = "balance_sheets"
    id = Column(Integer, primary_key=True)
    cash_quarter = Column(Float, default=0.0)
    total_assets_quarter = Column(Float, default=0.0)
    total_liabilities_quarter = Column(Float, default=0.0)
    working_capital_quarter = Column(Float, default=0.0)
    total_equity = Column(Float, default=0.0)
    long_term_debt_quarter = Column(Float, default=0.0)
    short_term_debt_quarter = Column(Float, default=0.0)
    total_debt_quarter = Column(Float, default=0.0)
    net_debt_quarter = Column(Float, default=0.0)
    fundamental = Relationship("Fundamental", backref="balance_sheet")


class CashFlowStatement(BaseModel):
    __tablename__ = "cash_flow_statements"
    id = Column(Integer, primary_key=True)
    cash_from_operations_ttm = Column(Float, default=0.0)
    cash_from_investing_ttm = Column(Float, default=0.0)
    cash_from_financing_ttm = Column(Float, default=0.0)
    capital_expenditure_ttm = Column(Float, default=0.0)
    free_cash_flow_ttm = Column(Float, default=0.0)
    fundamental = Relationship("Fundamental", backref="cash_flow_statement")


class PricePerformance(BaseModel):
    __tablename__ = "price_performances"
    id = Column(Integer, primary_key=True)
    one_week_price_returns = Column(Float, default=0.0)
    three_month_price_returns = Column(Float, default=0.0)
    one_month_price_returns = Column(Float, default=0.0)
    six_month_price_returns = Column(Float, default=0.0)
    one_year_price_returns = Column(Float, default=0.0)
    three_year_price_returns = Column(Float, default=0.0)
    five_year_price_returns = Column(Float, default=0.0)
    ten_year_price_returns = Column(Float, default=0.0)
    year_to_date_price_returns = Column(Float, default=0.0)
    fifty_two_week_high = Column(Float, default=0.0)
    fifty_two_week_low = Column(Float, default=0.0)
    fundamental = Relationship("Fundamental", backref="price_performance")


class Stats(BaseModel):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True)
    current_share_outstanding = Column(Float, default=0.0)
    market_cap = Column(Float, default=0.0)
    enterprise_value = Column(Float, default=0.0)
    fundamental = Relationship("Fundamental", backref="stat")
