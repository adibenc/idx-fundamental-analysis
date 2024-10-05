from dataclasses import dataclass
from datetime import datetime


@dataclass
class Sentiment:
    content: str = ""
    rate: float = ""
    category: str = ""
    posted_at: datetime = None
