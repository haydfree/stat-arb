import sys
import pandas as pd
from Data import Data
from ErrorHandler import ErrorHandler


class DataSet:
    __dataSet: list[Data]

    def __init__(self, **kwargs):
        dataSet: list[Data] = []
        for symbol, data in kwargs.items():
            setattr(self, f"__{symbol}", data)
            dataSet.append(data)

        self.setDataSet(dataSet)

    def getData(self,
                symbol: str) -> Data:
        ErrorHandler.validateInstrument(symbol)
        return self.getDataSet()[0] if self.getDataSet()[0].getSymbol() == symbol else self.getDataSet()[1]

    def setData(self,
                symbol: str,
                data: Data) -> None:
        ErrorHandler.validateInstrument(symbol)
        ErrorHandler.validateEnoughData(data.getData())
        setattr(self, f"__{symbol}", data)

    def getDataSet(self) -> list[Data]:
        return self.__dataSet

    def setDataSet(self,
                   dataSet: list[Data]) -> None:
        ErrorHandler.validateDataSet(dataSet)
        ErrorHandler.validateInstruments(dataSet[0].getSymbol(), dataSet[1].getSymbol())
        self.__dataSet = dataSet

    def cleanDataSet(self):
        dataSet: list[Data] = self.getDataSet()
        minimum: int = sys.maxsize

        for data in dataSet:
            if data.getData().size <= minimum:
                minimum = data.getData().size

        for idx, data in enumerate(dataSet):
            dataSet[idx].setData(data.getData().iloc[-minimum:])

        self.setDataSet(dataSet)
        return dataSet
