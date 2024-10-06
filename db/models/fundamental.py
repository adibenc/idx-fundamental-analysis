from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Relationship, mapped_column, Mapped, relationship

from db.models import BaseModel, FLOAT


class Fundamental(BaseModel):
    __tablename__ = "fundamentals"

    stats_id = mapped_column(ForeignKey("stats.id"))
    current_valuation_id = mapped_column(ForeignKey("current_valuations.id"))
    per_share_id = mapped_column(ForeignKey("per_shares.id"))
    solvency_id = mapped_column(ForeignKey("solvencies.id"))
    management_effectiveness_id = mapped_column(
        ForeignKey("management_effectivenesses.id")
    )
    profitability_id = mapped_column(ForeignKey("profitabilities.id"))
    growth_id = mapped_column(ForeignKey("growths.id"))
    dividend_id = mapped_column(ForeignKey("dividends.id"))
    market_rank_id = mapped_column(ForeignKey("market_ranks.id"))
    income_statement_id = mapped_column(ForeignKey("income_statements.id"))
    balance_sheet_id = mapped_column(ForeignKey("balance_sheets.id"))
    cash_flow_statement_id = mapped_column(ForeignKey("cash_flow_statements.id"))
    price_performance_id = mapped_column(ForeignKey("price_performances.id"))

    stock_ticker = mapped_column(ForeignKey("stocks.ticker"))


class CurrentValuation(BaseModel):
    __tablename__ = "current_valuations"

    current_pe_ratio_annual: Mapped[FLOAT]
    current_pe_ratio_ttm: Mapped[FLOAT]
    forward_pe_ratio: Mapped[FLOAT]
    ihsg_pe_ratio_ttm_median: Mapped[FLOAT]
    earnings_yield_ttm: Mapped[FLOAT]
    current_price_to_sales_ttm: Mapped[FLOAT]
    current_price_to_book_value: Mapped[FLOAT]
    current_price_to_cashflow_ttm: Mapped[FLOAT]
    current_price_to_free_cashflow_ttm: Mapped[FLOAT]
    ev_to_ebit_ttm: Mapped[FLOAT]
    ev_to_ebitda_ttm: Mapped[FLOAT]
    peg_ratio: Mapped[FLOAT]
    peg_ratio_3yr: Mapped[FLOAT]
    peg_forward: Mapped[FLOAT]

    fundamental = Relationship("Fundamental", backref="current_valuation")


class PerShare(BaseModel):
    __tablename__ = "per_shares"

    current_eps_ttm: Mapped[FLOAT]
    current_eps_annualised: Mapped[FLOAT]
    revenue_per_share_ttm: Mapped[FLOAT]
    cash_per_share_quarter: Mapped[FLOAT]
    current_book_value_per_share: Mapped[FLOAT]
    free_cashflow_per_share_ttm: Mapped[FLOAT]

    fundamental = Relationship("Fundamental", backref="per_share")


class Solvency(BaseModel):
    __tablename__ = "solvencies"

    current_ratio_quarter: Mapped[FLOAT]
    quick_ratio_quarter: Mapped[FLOAT]
    debt_to_equity_ratio_quarter: Mapped[FLOAT]
    lt_debt_equity_quarter: Mapped[FLOAT]
    total_liabilities_equity_quarter: Mapped[FLOAT]
    total_debt_total_assets_quarter: Mapped[FLOAT]
    financial_leverage_quarter: Mapped[FLOAT]
    interest_rate_coverage_ttm: Mapped[FLOAT]
    free_cash_flow_quarter: Mapped[FLOAT]
    altman_z_score_modified: Mapped[FLOAT]
    fundamental: Mapped["Fundamental"] = relationship(backref="solvency")


class ManagementEffectiveness(BaseModel):
    __tablename__ = "management_effectivenesses"

    return_on_assets_ttm: Mapped[FLOAT]
    return_on_equity_ttm: Mapped[FLOAT]
    return_on_capital_employed_ttm: Mapped[FLOAT]
    return_on_invested_capital_ttm: Mapped[FLOAT]
    days_sales_outstanding_quarter: Mapped[FLOAT]
    days_inventory_quarter: Mapped[FLOAT]
    days_payables_outstanding_quarter: Mapped[FLOAT]
    cash_conversion_cycle_quarter: Mapped[FLOAT]
    receivables_turnover_quarter: Mapped[FLOAT]
    asset_turnover_ttm: Mapped[FLOAT]
    inventory_turnover_ttm: Mapped[FLOAT]

    fundamental: Mapped["Fundamental"] = relationship(
        backref="management_effectiveness"
    )


class Profitability(BaseModel):
    __tablename__ = "profitabilities"

    gross_profit_margin_quarter: Mapped[FLOAT]
    operating_profit_margin_quarter: Mapped[FLOAT]
    net_profit_margin_quarter: Mapped[FLOAT]

    fundamental: Mapped["Fundamental"] = relationship(backref="profitability")


class Growth(BaseModel):
    __tablename__ = "growths"

    revenue_quarter_yoy_growth: Mapped[FLOAT]
    gross_profit_quarter_yoy_growth: Mapped[FLOAT]
    net_income_quarter_yoy_growth: Mapped[FLOAT]
    fundamental: Mapped["Fundamental"] = relationship(backref="growth")


class Dividend(BaseModel):
    __tablename__ = "dividends"

    dividend: Mapped[FLOAT]
    dividend_ttm: Mapped[FLOAT]
    payout_ratio: Mapped[FLOAT]
    dividend_yield: Mapped[FLOAT]
    latest_dividend_ex_date = mapped_column(String, default="")

    fundamental: Mapped["Fundamental"] = relationship(backref="dividend")


class MarketRank(BaseModel):
    __tablename__ = "market_ranks"

    piotroski_f_score: Mapped[FLOAT]
    eps_rating: Mapped[FLOAT]
    relative_strength_rating: Mapped[FLOAT]
    rank_market_cap: Mapped[FLOAT]
    rank_current_pe_ratio_ttm: Mapped[FLOAT]
    rank_earnings_yield: Mapped[FLOAT]
    rank_p_s: Mapped[FLOAT]
    rank_p_b: Mapped[FLOAT]
    rank_near_52_weeks_high: Mapped[FLOAT]

    fundamental: Mapped["Fundamental"] = relationship(backref="market_rank")


class IncomeStatement(BaseModel):
    __tablename__ = "income_statements"

    revenue_ttm: Mapped[FLOAT]
    gross_profit_ttm: Mapped[FLOAT]
    ebitda_ttm: Mapped[FLOAT]
    net_income_ttm: Mapped[FLOAT]

    fundamental: Mapped["Fundamental"] = relationship(backref="income_statement")


class BalanceSheet(BaseModel):
    __tablename__ = "balance_sheets"

    cash_quarter: Mapped[FLOAT]
    total_assets_quarter: Mapped[FLOAT]
    total_liabilities_quarter: Mapped[FLOAT]
    working_capital_quarter: Mapped[FLOAT]
    total_equity: Mapped[FLOAT]
    long_term_debt_quarter: Mapped[FLOAT]
    short_term_debt_quarter: Mapped[FLOAT]
    total_debt_quarter: Mapped[FLOAT]
    net_debt_quarter: Mapped[FLOAT]

    fundamental: Mapped["Fundamental"] = relationship(backref="balance_sheet")


class CashFlowStatement(BaseModel):
    __tablename__ = "cash_flow_statements"

    cash_from_operations_ttm: Mapped[FLOAT]
    cash_from_investing_ttm: Mapped[FLOAT]
    cash_from_financing_ttm: Mapped[FLOAT]
    capital_expenditure_ttm: Mapped[FLOAT]
    free_cash_flow_ttm: Mapped[FLOAT]

    fundamental: Mapped["Fundamental"] = relationship(backref="cash_flow_statement")


class PricePerformance(BaseModel):
    __tablename__ = "price_performances"

    one_week_price_returns: Mapped[FLOAT]
    three_month_price_returns: Mapped[FLOAT]
    one_month_price_returns: Mapped[FLOAT]
    six_month_price_returns: Mapped[FLOAT]
    one_year_price_returns: Mapped[FLOAT]
    three_year_price_returns: Mapped[FLOAT]
    five_year_price_returns: Mapped[FLOAT]
    ten_year_price_returns: Mapped[FLOAT]
    year_to_date_price_returns: Mapped[FLOAT]
    fifty_two_week_high: Mapped[FLOAT]
    fifty_two_week_low: Mapped[FLOAT]

    fundamental: Mapped["Fundamental"] = relationship(backref="price_performance")


class Stats(BaseModel):
    __tablename__ = "stats"

    current_share_outstanding: Mapped[FLOAT]
    market_cap: Mapped[FLOAT]
    enterprise_value: Mapped[FLOAT]

    fundamental: Mapped["Fundamental"] = relationship(backref="stat")
