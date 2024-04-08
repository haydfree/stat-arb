import datetime
import pandas as pd
from DataSource import DataSource
from Instrument import Instrument
from ErrorHandler import ErrorHandler


class Data:
    __dataSource: DataSource
    __instrument: Instrument
    __data: pd.DataFrame

    __symbol: str
    __startDate: datetime.datetime
    __endDate: datetime.datetime
    __timeframe: str

    def __init__(self,
                 dataSource: DataSource,
                 instrument: Instrument,
                 startDate: datetime,
                 endDate: datetime,
                 timeframe: str):
        self.__dataSource = dataSource
        self.__instrument = instrument

        self.setSymbol(instrument.getSymbol())
        self.setStartDate(startDate)
        self.setEndDate(endDate)
        self.setTimeframe(timeframe)

    def getDataSource(self) -> DataSource:
        return self.__dataSource

    def setDataSource(self,
                      dataSource: DataSource) -> None:
        ErrorHandler.validateDataSource(dataSource)
        self.__dataSource = dataSource

    def getInstrument(self) -> Instrument:
        return self.__instrument

    def setInstrument(self,
                      instrument: Instrument) -> None:
        ErrorHandler.validateInstrument(instrument)
        self.__instrument = instrument

    def getData(self) -> pd.DataFrame:
        return self.__data

    def setData(self,
                data: pd.DataFrame) -> None:
        ErrorHandler.validateEnoughData(data)
        self.__data = data

    def getSymbol(self) -> str:
        return self.__symbol

    def setSymbol(self,
                  symbol: str) -> None:
        ErrorHandler.validateInstrument(symbol)
        self.__symbol = symbol

    def getStartDate(self) -> datetime.datetime:
        return self.__startDate

    def setStartDate(self,
                     startDate: datetime.datetime) -> None:
        ErrorHandler.validateDate(startDate)
        self.__startDate = startDate

    def getEndDate(self) -> datetime.datetime:
        return self.__endDate

    def setEndDate(self,
                   endDate: datetime.datetime) -> None:
        ErrorHandler.validateDate(endDate)
        self.__endDate = endDate

    def getTimeframe(self) -> str:
        return self.__timeframe

    def setTimeframe(self,
                     timeframe: str) -> None:
        ErrorHandler.validateTimeframe(timeframe)
        self.__timeframe = timeframe

    def downloadData(self) -> pd.DataFrame:
        dataSource: DataSource = self.getDataSource()
        symbol: str = self.getSymbol()
        startDate: datetime.datetime = self.getStartDate()
        endDate: datetime.datetime = self.getEndDate()
        timeframe: str = self.getTimeframe()

        data: pd.DataFrame = dataSource.downloadData(symbol=symbol,
                                                     startDate=startDate,
                                                     endDate=endDate,
                                                     timeframe=timeframe)

        self.setData(data)
        return data

    def cleanData(self) -> pd.DataFrame:
        data: pd.DataFrame = self.getData()
        symbol: str = self.getSymbol()

        data = data["Close"]
        data.name = symbol
        data.ffill(inplace=True)

        self.setData(data)
        return data

