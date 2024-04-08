from Data import Data
from Instrument import Instrument
from ErrorHandler import ErrorHandler
import pandas as pd


class Pair:
    __instrument1: Instrument
    __instrument1Data: Data

    __instrument2: Instrument
    __instrument2Data: Data

    __pairName: str
    __window: int
    __spread: pd.Series
    __standardizedSpread: pd.Series

    def __init__(self,
                 data1: Data,
                 data2: Data,
                 window: int):
        self.setInstrument1(data1.getInstrument())
        self.setInstrument1Data(data1)
        self.setInstrument2(data2.getInstrument())
        self.setInstrument2Data(data2)
        self.setWindow(window)
        self.setPairName(f"{self.__instrument1.getSymbol()}_{self.__instrument2.getSymbol()}")

    def getInstrument1(self) -> Instrument:
        return self.__instrument1

    def setInstrument1(self,
                       instrument: Instrument) -> None:
        ErrorHandler.validateInstrument(instrument.getSymbol())
        self.__instrument1 = instrument

    def getInstrument2(self) -> Instrument:
        return self.__instrument2

    def setInstrument2(self,
                       instrument: Instrument) -> None:
        ErrorHandler.validateInstrument(instrument.getSymbol())
        self.__instrument2 = instrument

    def getInstrument1Data(self) -> Data:
        return self.__instrument1Data

    def setInstrument1Data(self,
                           data: Data) -> None:
        ErrorHandler.validateEnoughData(data.getData())
        self.__instrument1Data = data

    def getInstrument2Data(self) -> Data:
        return self.__instrument2Data

    def setInstrument2Data(self,
                           data: Data) -> None:
        ErrorHandler.validateEnoughData(data.getData())
        self.__instrument2Data = data

    def getPairName(self) -> str:
        return self.__pairName

    def setPairName(self,
                    pairName: str) -> None:
        ErrorHandler.validatePairName(pairName)
        self.__pairName = pairName

    def getWindow(self) -> int:
        return self.__window

    def setWindow(self,
                  window: int) -> None:
        ErrorHandler.validateInteger(window)
        self.__window = window

    def getSpread(self) -> pd.Series:
        return self.__spread

    def setSpread(self,
                  spread: pd.Series) -> None:
        ErrorHandler.validateSpread(spread)
        self.__spread = spread

    def getStandardizedSpread(self) -> pd.Series:
        return self.__standardizedSpread

    def setStandardizedSpread(self,
                              standardizedSpread: pd.Series) -> None:
        ErrorHandler.validateSpread(standardizedSpread)
        self.__standardizedSpread = standardizedSpread

    def calculateSpread(self) -> pd.Series:
        instrument1Data = self.getInstrument1Data().getData()
        instrument2Data = self.getInstrument2Data().getData()

        spread: pd.Series() = (instrument1Data - instrument2Data)

        spread.name = self.getPairName()

        self.setSpread(spread.dropna())
        return spread

    def calculateStandardizedSpread(self) -> pd.Series:
        spread: pd.Series = self.getSpread()
        window: int = self.getWindow()

        zScore = ((spread - spread.rolling(window=window).mean()) /
                  spread.rolling(window=window).std())
        self.setStandardizedSpread(zScore.dropna())
        return zScore
