from abc import abstractmethod


class BuilderInterface:
    @abstractmethod
    def insert_stock(self):
        pass

    @abstractmethod
    def insert_key_statistic(self):
        pass

    @abstractmethod
    def insert_analysis(self):
        pass

    @abstractmethod
    def insert_sentiment(self):
        pass
