from sqlalchemy import Column, Float, Integer, ForeignKey

from db import BaseModel


class KeyAnalysis(BaseModel):
    __tablename__ = "key_analysis"

    normal_price = Column(Float, default=0.0)
    price_to_equity_discount = Column(Float, default=0.0)
    relative_pe_ratio_ttm = Column(Float, default=0.0)
    eps_growth = Column(Float, default=0.0)
    debt_to_total_assets_ratio = Column(Float, default=0.0)
    liquidity_differential = Column(Float, default=0.0)
    cce = Column(Float, default=0.0)
    operating_efficiency = Column(Float, default=0.0)
    dividend_payout_efficiency = Column(Float, default=0.0)
    yearly_price_change = Column(Float, default=0.0)
    composite_rank = Column(Float, default=0.0)
    net_debt_to_equity_ratio = Column(Float, default=0.0)

    stock_id = Column(Integer, ForeignKey("stocks.id"))
