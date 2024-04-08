import pandas as pd
from ErrorHandler import ErrorHandler


class Instrument:
    __symbol: str
    __data: pd.DataFrame

    def __init__(self,
                 symbol: str):
        self.setSymbol(symbol)

    def getSymbol(self) -> str:
        return self.__symbol

    def setSymbol(self,
                  symbol: str) -> None:
        ErrorHandler.validateInstrument(symbol)
        self.__symbol = symbol

    def getData(self) -> pd.DataFrame:
        return self.__data

    def setData(self,
                data: pd.DataFrame) -> None:
        ErrorHandler.validateEnoughData(data)
        self.__data = data

