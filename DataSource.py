import yfinance
import pandas as pd
import datetime
from ErrorHandler import ErrorHandler


class DataSource:
    __source: str

    def __init__(self,
                 source: str):
        ErrorHandler.validateDataSource(source)
        self.__source = source

    def getSource(self) -> str:
        return self.__source

    def setSource(self,
                  source: str) -> None:
        ErrorHandler.validateDataSource(source)
        self.__source = source

    def downloadData(self,
                     symbol: str,
                     startDate: datetime.datetime,
                     endDate: datetime.datetime,
                     timeframe: str) -> pd.DataFrame:
        source: str = self.getSource()
        ErrorHandler.validateDataSource(source)
        ErrorHandler.validateDateRange(startDate=startDate,
                                       endDate=endDate,
                                       timeframe=timeframe)

        if source == "yahoo":
            return yfinance.Ticker(symbol).history(start=startDate,
                                                   end=endDate,
                                                   interval=timeframe)
