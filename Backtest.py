import pandas as pd
from Strategy import Strategy
import matplotlib.pyplot as plt


class Backtest:
    __strategy: Strategy

    def __init__(self,
                 strategy: Strategy):
        self.__strategy = strategy

    def getStrategy(self) -> Strategy:
        return self.__strategy

    def setStrategy(self,
                    strategy: Strategy) -> None:
        self.__strategy = strategy

    def showInfo(self) -> pd.DataFrame:
        strategy: Strategy = self.getStrategy()
        pair: str = strategy.getPair().getPairName()
        closedTradesInfo: pd.DataFrame = strategy.createClosedTradesInfo()

        plt.plot(strategy.getStandardizedSpread())
        plt.axhline(strategy.getEntryThreshold(), color="black")
        plt.axhline(-strategy.getEntryThreshold(), color="black")
        plt.plot(strategy.getExitThreshold(), color="black")
        plt.title(f"{pair} standardized spread")
        plt.xlabel("Date")
        plt.ylabel("Spread")
        plt.show()

        plt.plot(closedTradesInfo["cumSum"])
        plt.title("Profit / Loss")
        plt.xlabel("Trades")
        plt.ylabel("Equity")
        plt.show()

        return strategy.getClosedTradesInfo()

