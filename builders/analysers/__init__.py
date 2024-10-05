from builders.analysers.fundamental_analyser import FundamentalAnalyser
from builders.analysers.sentiment_analyser import SentimentAnalyser
from builders.excel import Excel
from builders.spreadsheet import Spreadsheet
from schemas.stock import Stock


class Analyser:
    def __init__(self, stocks: [Stock]):
        self.stocks = stocks
        self.fundamental_analyser = FundamentalAnalyser(stocks=stocks)
        self.sentiment_analyser = SentimentAnalyser(stocks=stocks)

    def build(self, output: str, title: str):
        if output == "excel":
            self._build_output(Excel, title)
        elif output == "spreadsheet":
            self._build_output(Spreadsheet, title)
        else:
            raise ValueError("Unsupported output method")

    def _build_output(self, builder_class, title):
        builder = builder_class(
            title=title,
            fundamental_analyser=self.fundamental_analyser,
            sentiment_analyser=self.sentiment_analyser,
        )
        builder.insert_analysis()
        builder.insert_stock()
        builder.insert_key_statistic()
        builder.insert_sentiment()

        if isinstance(builder, Excel):
            builder.save()
