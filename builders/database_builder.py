from builders.builder_interface import BuilderInterface
from db import (
    StockPrice,
    Sentiment,
    KeyAnalysis,
    CurrentValuation,
    PerShare,
    Solvency,
    ManagementEffectiveness,
    Profitability,
    Growth,
    Dividend,
    MarketRank,
    IncomeStatement,
    BalanceSheet,
    CashFlowStatement,
    PricePerformance,
    Stat,
    Fundamental,
    # CorpAction,
)
from db.models.stock import Stock

from db.session import get_session, get_session_a
from schemas.stock import Stock as StockSchema


class DatabaseBuilder(BuilderInterface):
    def __init__(self, stocks=[StockSchema]):
        self.stocks = stocks

    def insert_stock(self):
        for stock in self.stocks:
            with get_session_a() as session:
                stock_model = Stock(
                    ticker=stock.ticker,
                    name=stock.name,
                    ipo_date=stock.ipo_date,
                    note=stock.note,
                    market_cap=stock.market_cap,
                    home_page=stock.home_page,
                )

                session.add(stock_model)
    
    def insert_dividend(self):
        for stock in self.stocks:
            with get_session_a() as session:
                dividend = Dividend(**stock.fundamental.dividend.to_dict())

                session.add(dividend)

                # Create the Fundamental instance
                fundamental = Fundamental(
                    dividend_id=dividend.id,
                    stock_ticker=stock.ticker,
                )

                # Add the Fundamental instance to the session
                session.add(fundamental)

    def insert_key_statistic(self):

        for stock in self.stocks:
            with get_session() as session:
                # Create instances of related models
                current_valuation = CurrentValuation(
                    **stock.fundamental.current_valuation.to_dict()
                )
                per_share = PerShare(**stock.fundamental.per_share.to_dict())
                solvency = Solvency(**stock.fundamental.solvency.to_dict())
                management_effectiveness = ManagementEffectiveness(
                    **stock.fundamental.management_effectiveness.to_dict()
                )
                profitability = Profitability(
                    **stock.fundamental.profitability.to_dict()
                )
                growth = Growth(**stock.fundamental.growth.to_dict())
                dividend = Dividend(**stock.fundamental.dividend.to_dict())
                market_rank = MarketRank(**stock.fundamental.market_rank.to_dict())
                income_statement = IncomeStatement(
                    **stock.fundamental.income_statement.to_dict()
                )
                balance_sheet = BalanceSheet(
                    **stock.fundamental.balance_sheet.to_dict()
                )
                cash_flow_statement = CashFlowStatement(
                    **stock.fundamental.cash_flow_statement.to_dict()
                )
                price_performance = PricePerformance(
                    **stock.fundamental.price_performance.to_dict()
                )
                stat = Stat(**stock.fundamental.stat.to_dict())

                # Add all instances to the session
                session.add_all(
                    [
                        current_valuation,
                        per_share,
                        solvency,
                        management_effectiveness,
                        profitability,
                        growth,
                        dividend,
                        market_rank,
                        income_statement,
                        balance_sheet,
                        cash_flow_statement,
                        price_performance,
                        stat,
                    ]
                )

                session.commit()

                # Create the Fundamental instance
                fundamental = Fundamental(
                    stat_id=stat.id,
                    current_valuation_id=current_valuation.id,
                    per_share_id=per_share.id,
                    solvency_id=solvency.id,
                    management_effectiveness_id=management_effectiveness.id,
                    profitability_id=profitability.id,
                    growth_id=growth.id,
                    dividend_id=dividend.id,
                    market_rank_id=market_rank.id,
                    income_statement_id=income_statement.id,
                    balance_sheet_id=balance_sheet.id,
                    cash_flow_statement_id=cash_flow_statement.id,
                    price_performance_id=price_performance.id,
                    stock_ticker=stock.ticker,
                )

                # Add the Fundamental instance to the session
                session.add(fundamental)

    def insert_key_analysis(self):
        for stock in self.stocks:
            with get_session() as session:
                key_analysis = KeyAnalysis(
                    normal_price=stock.key_analysis.normal_price,
                    price_to_equity_discount=stock.key_analysis.price_to_equity_discount,
                    relative_pe_ratio_ttm=stock.key_analysis.relative_pe_ratio_ttm,
                    eps_growth=stock.key_analysis.eps_growth,
                    debt_to_total_assets_ratio=stock.key_analysis.debt_to_total_assets_ratio,
                    liquidity_differential=stock.key_analysis.liquidity_differential,
                    cce=stock.key_analysis.cce,
                    operating_efficiency=stock.key_analysis.operating_efficiency,
                    dividend_payout_efficiency=stock.key_analysis.dividend_payout_efficiency,
                    yearly_price_change=stock.key_analysis.yearly_price_change,
                    composite_rank=stock.key_analysis.composite_rank,
                    stock_ticker=stock.ticker,
                )

                session.add(key_analysis)

    def insert_sentiment(self):
        for stock in self.stocks:
            for sentiment in stock.sentiment:
                with get_session() as session:
                    sentiment = Sentiment(
                        content=sentiment.content,
                        rate=sentiment.rate,
                        stock_ticker=stock.ticker,
                        posted_at=sentiment.posted_at,
                    )
                    session.add(sentiment)

    def insert_stock_price(self):
        for stock in self.stocks:
            with get_session() as session:
                stock_price = StockPrice(
                    stock_ticker=stock.ticker,
                    price=stock.stock_price.price,
                    volume=stock.stock_price.volume,
                    percentage_change=stock.stock_price.percentage_change,
                    average=stock.stock_price.average,
                    close=stock.stock_price.close,
                    high=stock.stock_price.high,
                    low=stock.stock_price.low,
                    open=stock.stock_price.open,
                    ara=stock.stock_price.ara,
                    arb=stock.stock_price.arb,
                    frequency=stock.stock_price.frequency,
                    fsell=stock.stock_price.fsell,
                    fbuy=stock.stock_price.fbuy,
                )

                session.add(stock_price)
    
    def insert_corp_action(self):
        try:
            for stock in self.stocks:
                for action in stock.corp_actions:
                    with get_session() as session:
                        corp_action = CorpAction(
                            stock_ticker=stock.ticker,
                            company_id=action["action_info"]["rups"]["company_id"],
                            company_symbol=action["action_info"]["rups"]["company_symbol"],
                            rups_date=action["action_info"]["rups"]["rups_date"],
                            rups_venue=action["action_info"]["rups"]["rups_venue"],
                            rups_time=action["action_info"]["rups"]["rups_time"],
                        )
                        session.add(corp_action)
        except Exception:
            print("insert corp act")

    def insert_corp_action_df(self, corp_actions: list):
        """
        Insert corporate action data into the database.
        """
        try:
            with database.engine.begin() as conn:
                for action in corp_actions:
                    corp_action = CorpAction(
                        # company_id=action["action_info"]["rups"]["company_id"],
                        # company_symbol=action["action_info"]["rups"]["company_symbol"],
                        rups_date=action["action_info"]["rups"]["rups_date"],
                        rups_venue=action["action_info"]["rups"]["rups_venue"],
                        rups_time=action["action_info"]["rups"]["rups_time"],
                    )
                    conn.add(corp_action)
                conn.commit()
            logger.info("Corporate action data inserted successfully.")
        except Exception as e:
            logger.error(f"Failed to insert corporate action data: {e}")