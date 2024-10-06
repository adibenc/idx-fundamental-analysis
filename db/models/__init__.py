from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True  # This tells SQLAlchemy not to create a table for this class

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now(ZoneInfo("UTC")))

    def save(self, session):
        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()
