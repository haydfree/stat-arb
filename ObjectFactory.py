from typing import Union

from Data import Data
from DataSet import DataSet
from DataSource import DataSource
from Instrument import Instrument
from Model import Model
from Pair import Pair
from Strategy import Strategy
from Backtest import Backtest
from Utils import Utils
from ErrorHandler import ErrorHandler
import datetime
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt


class ObjectFactory:
    __name: str
    __data1: Data
    __data2: Data
    __dataSet: DataSet
    __dataSource: DataSource
    __instrument1: Instrument
    __instrument2: Instrument
    __model: Model
    __pair: Pair
    __strategy: Strategy
    __backtest: Backtest
    __startDate: datetime
    __endDate: datetime
    __timeframe: str
    __entryThreshold: int
    __window: int
    __modelTestResults: pd.DataFrame
    __predictedData: pd.Series
    __residuals: pd.Series

    __plot1Data: pd.Series
    __plot2Data: pd.Series

    def __init__(self,
                 name: str):
        self.__name = name

    def run(self,
            values: dict) -> None:
        dataSource: str = values["dataSource"]
        instrument1: str = values["instrument1"]
        instrument2: str = values["instrument2"]

        ErrorHandler.validateDateFormat(values["startDate"])
        ErrorHandler.validateDateFormat(values["endDate"])
        startDate: datetime = datetime.datetime.strptime(values["startDate"], "%Y-%m-%d")
        endDate: datetime = datetime.datetime.strptime(values["endDate"], "%Y-%m-%d")

        timeframe = values["timeframe"]
        entryThreshold: int = int(values["entryThreshold"])
        window: int = int(values["window"])

        dataSource: DataSource = DataSource(source=dataSource)
        self.setDataSource(dataSource=dataSource)

        instrument1: Instrument = Instrument(symbol=instrument1)
        self.setInstrument1(instrument1=instrument1)

        instrument2: Instrument = Instrument(symbol=instrument2)
        self.setInstrument2(instrument2=instrument2)

        self.setStartDate(startDate=startDate)
        self.setEndDate(endDate=endDate)
        self.setTimeframe(timeframe=timeframe)

        data1: Data = Data(dataSource=dataSource,
                           instrument=instrument1,
                           startDate=startDate,
                           endDate=endDate,
                           timeframe=timeframe)
        data2: Data = Data(dataSource=dataSource,
                           instrument=instrument2,
                           startDate=startDate,
                           endDate=endDate,
                           timeframe=timeframe)

        data1.downloadData()
        data2.downloadData()
        data1.cleanData()
        data2.cleanData()

        dataSet: DataSet = DataSet(data1=data1,
                                   data2=data2)
        data1, data2 = dataSet.cleanDataSet()
        self.setData1(data1=data1)
        self.setData2(data2=data2)
        self.setDataSet(dataSet=dataSet)

        self.setEntryThreshold(entryThreshold=entryThreshold)
        self.setWindow(window=window)

        pair: Pair = Pair(data1=data1,
                          data2=data2,
                          window=window)
        pair.calculateSpread()
        pair.calculateStandardizedSpread()
        self.setPair(pair=pair)

        model: Model = Model(pair=pair)
        model.predict(pair.getStandardizedSpread())
        fairMarketValue: pd.Series = model.getFairMarketValue()
        self.setModel(model=model)

        strategy = Strategy(pair=pair,
                            entryThreshold=entryThreshold,
                            exitThreshold=fairMarketValue)
        strategy.findTrades()
        self.setStrategy(strategy=strategy)

        backtest: Backtest = Backtest(strategy=strategy)
        self.setBacktest(backtest=backtest)
        strategy.createClosedTradesInfo()

        modelTestResults, predictedData, residuals = Utils.testModelAccuracy(model=model)
        self.setModelTestResults(modelTestResults=modelTestResults)
        self.setPredictedData(predictedData=predictedData)
        self.setResiduals(residuals=residuals)

        plot1Data: pd.Series = strategy.getStandardizedSpread()
        plot2Data: pd.Series = strategy.getClosedTradesInfo()["cumSum"]
        self.setPlot1Data(plot1Data=plot1Data)
        self.setPlot2Data(plot2Data=plot2Data)

    def getName(self) -> str:
        return self.__name

    def setName(self,
                name: str) -> None:
        self.__name = name

    def getData1(self) -> Data:
        return self.__data1

    def setData1(self,
                 data1: Data) -> None:
        self.__data1 = data1

    def getData2(self) -> Data:
        return self.__data2

    def setData2(self,
                 data2: Data) -> None:
        self.__data2 = data2

    def getDataSource(self) -> DataSource:
        return self.__dataSource

    def setDataSource(self,
                      dataSource: DataSource) -> None:
        self.__dataSource = dataSource

    def getInstrument1(self) -> Instrument:
        return self.__instrument1

    def setInstrument1(self,
                       instrument1: Instrument) -> None:
        self.__instrument1 = instrument1

    def getInstrument2(self) -> Instrument:
        return self.__instrument2

    def setInstrument2(self,
                       instrument2: Instrument) -> None:
        self.__instrument2 = instrument2

    def getStartDate(self) -> datetime:
        return self.__startDate

    def setStartDate(self,
                     startDate: datetime) -> None:
        self.__startDate = startDate

    def getEndDate(self) -> datetime:
        return self.__endDate

    def setEndDate(self,
                   endDate: datetime) -> None:
        self.__endDate = endDate

    def getTimeframe(self) -> str:
        return self.__timeframe

    def setTimeframe(self,
                     timeframe: str) -> None:
        self.__timeframe = timeframe

    def getDataSet(self) -> DataSet:
        return self.__dataSet

    def setDataSet(self,
                   dataSet: DataSet) -> None:
        self.__dataSet = dataSet

    def getModel(self) -> Model:
        return self.__model

    def setModel(self,
                 model: Model) -> None:
        self.__model = model

    def getPair(self) -> Pair:
        return self.__pair

    def setPair(self,
                pair: Pair) -> None:
        self.__pair = pair

    def getStrategy(self) -> Strategy:
        return self.__strategy

    def setStrategy(self,
                    strategy: Strategy) -> None:
        self.__strategy = strategy

    def getBacktest(self) -> Backtest:
        return self.__backtest

    def setBacktest(self,
                    backtest: Backtest) -> None:
        self.__backtest = backtest

    def getEntryThreshold(self) -> int:
        return self.__entryThreshold

    def setEntryThreshold(self,
                          entryThreshold: int) -> None:
        self.__entryThreshold = entryThreshold

    def getWindow(self) -> int:
        return self.__window

    def setWindow(self,
                  window: int) -> None:
        self.__window = window

    def getPlot1Data(self) -> pd.Series:
        return self.__plot1Data

    def setPlot1Data(self,
                     plot1Data: pd.Series) -> None:
        self.__plot1Data = plot1Data

    def getPlot2Data(self) -> pd.Series:
        return self.__plot2Data

    def setPlot2Data(self,
                     plot2Data: pd.Series) -> None:
        self.__plot2Data = plot2Data

    def getModelTestResults(self) -> pd.DataFrame:
        return self.__modelTestResults

    def setModelTestResults(self,
                            modelTestResults: pd.DataFrame) -> None:
        self.__modelTestResults = modelTestResults

    def getPredictedData(self) -> pd.Series:
        return self.__predictedData

    def setPredictedData(self,
                         predictedData: pd.Series) -> None:
        self.__predictedData = predictedData

    def getResiduals(self) -> pd.Series:
        return self.__residuals

    def setResiduals(self,
                     residuals: pd.Series) -> None:
        self.__residuals = residuals
