from sqlalchemy import create_engine

from db.models import Base
from db.models.fundamental import *
from db.models.key_analysis import KeyAnalysis
from db.models.sentiment import Sentiment
from db.models.stock import Stock
from db.models.stock_price import StockPrice


class DB:
    def __init__(self):
        self._engine = create_engine("sqlite:///./db/idx-fundamental.db")

    def setup_db(self, is_drop_table: bool = False):
        with self._engine.begin() as conn:
            if is_drop_table:
                # Drop all tables in the database
                Base.metadata.drop_all(conn)

            # Create all tables in the database
            Base.metadata.create_all(conn)

    @property
    def engine(self):
        return self._engine
