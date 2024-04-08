import datetime
from ErrorHandler import ErrorHandler


class Trade:
    __symbol: str
    __pairName: str
    __pairTradeDirection: int
    __entryPrice: float
    __exitPrice: float
    __entryTime: datetime.datetime
    __exitTime: datetime.datetime
    __direction: int
    __volume: float
    __profitLoss: float

    def __init__(self,
                 symbol: str,
                 pairName: str,
                 pairTradeDirection: int,
                 entryPrice: float,
                 entryTime: datetime.datetime,
                 direction: int,
                 volume: float):
        self.setSymbol(symbol)
        self.setPairName(pairName)
        self.setPairTradeDirection(pairTradeDirection)
        self.setEntryPrice(entryPrice)
        self.setEntryTime(entryTime)
        self.setDirection(direction)
        self.setVolume(volume)

    def getSymbol(self) -> str:
        return self.__symbol

    def setSymbol(self,
                  symbol: str) -> None:
        ErrorHandler.validateInstrument(symbol)
        self.__symbol = symbol

    def getPairName(self) -> str:
        return self.__pairName

    def setPairName(self,
                    pairName: str) -> None:
        ErrorHandler.validatePairName(pairName)
        self.__pairName = pairName

    def getPairTradeDirection(self) -> int:
        return self.__pairTradeDirection

    def setPairTradeDirection(self,
                              pairTradeDirection: int) -> None:
        ErrorHandler.validateTradeDirection(pairTradeDirection)
        self.__pairTradeDirection = pairTradeDirection

    def getEntryPrice(self) -> float:
        return self.__entryPrice

    def setEntryPrice(self,
                      entryPrice: float) -> None:
        ErrorHandler.validateNumber(entryPrice)
        ErrorHandler.validatePositive(entryPrice)
        self.__entryPrice = entryPrice

    def getExitPrice(self) -> float:
        return self.__exitPrice

    def setExitPrice(self,
                     exitPrice: float) -> None:
        ErrorHandler.validateNumber(exitPrice)
        ErrorHandler.validatePositive(exitPrice)
        self.__exitPrice = exitPrice

    def getEntryTime(self) -> datetime.datetime:
        return self.__entryTime

    def setEntryTime(self,
                     entryTime: datetime.datetime) -> None:
        ErrorHandler.validateDate(entryTime)
        self.__entryTime = entryTime

    def getExitTime(self) -> datetime.datetime:
        return self.__exitTime

    def setExitTime(self,
                    exitTime: datetime.datetime) -> None:
        ErrorHandler.validateDate(exitTime)
        self.__exitTime = exitTime

    def getDirection(self) -> int:
        return self.__direction

    def setDirection(self,
                     direction: int) -> None:
        ErrorHandler.validateTradeDirection(direction)
        self.__direction = direction

    def getVolume(self) -> float:
        return self.__volume

    def setVolume(self,
                  volume: float) -> None:
        ErrorHandler.validateNumber(volume)
        ErrorHandler.validatePositive(volume)
        self.__volume = volume

    def getProfitLoss(self) -> float:
        return self.__profitLoss

    def setProfitLoss(self,
                      profitLoss: float) -> None:
        ErrorHandler.validateNumber(profitLoss)
        self.__profitLoss = profitLoss

    def calculateProfitLoss(self) -> float:
        entryPrice: float = self.getEntryPrice()
        exitPrice: float = self.getExitPrice()
        direction: int = self.getDirection()
        volume: float = self.getVolume()

        if direction == 1:
            profitLoss: float = (exitPrice - entryPrice) * volume
        elif direction == -1:
            profitLoss: float = (entryPrice - exitPrice) * volume
        else:
            profitLoss: float = 0

        self.setProfitLoss(profitLoss)
        return profitLoss
