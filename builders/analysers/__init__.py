from builders.analysers.fundamental_analyser import FundamentalAnalyser
from builders.analysers.key_analysis_analyser import KeyAnalysisAnalyser
from builders.analysers.sentiment_analyser import SentimentAnalyser
from builders.analysers.stock_price_analyser import StockPriceAnalyser
from builders.excel import Excel
from builders.spreadsheet import Spreadsheet
from schemas.stock import Stock


class Analyser:
    def __init__(self, stocks: [Stock]):
        self.stocks = stocks
        self.fundamental_analyser = FundamentalAnalyser(stocks=stocks)
        self.sentiment_analyser = SentimentAnalyser(stocks=stocks)
        self.key_analysis_analyser = KeyAnalysisAnalyser(stocks=stocks)
        self.stock_price_analyser = StockPriceAnalyser(stocks=stocks)

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
            key_analysis_analyser=self.key_analysis_analyser,
            stock_price_analyser=self.stock_price_analyser,
        )
        builder.insert_key_analysis()
        builder.insert_stock()
        builder.insert_stock_price()
        builder.insert_key_statistic()
        builder.insert_sentiment()

        if isinstance(builder, Excel):
            builder.save()
