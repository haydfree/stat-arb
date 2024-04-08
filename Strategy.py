import datetime

from Pair import Pair
from Trade import Trade
from Data import Data
from ErrorHandler import ErrorHandler
import pandas as pd


class Strategy:
    __spread: pd.Series
    __standardizedSpread: pd.Series

    __pair: Pair

    __entryThreshold: int
    __exitThreshold: pd.Series

    __openTrades: list[Trade]
    __closedTrades: list[Trade]

    __closedTradesInfo: pd.DataFrame

    def __init__(self,
                 pair: Pair,
                 entryThreshold: int,
                 exitThreshold: pd.Series):
        self.setSpread(pair.getSpread())
        self.setStandardizedSpread(pair.getStandardizedSpread())
        self.setPair(pair)
        self.setEntryThreshold(entryThreshold)
        self.setExitThreshold(exitThreshold)
        self.setClosedTradesInfo(pd.DataFrame())

        self.__openTrades = []
        self.__closedTrades = []

    def getSpread(self) -> pd.Series:
        return self.__spread

    def setSpread(self,
                  spread: pd.Series) -> None:
        ErrorHandler.validateSpread(spread)
        ErrorHandler.validateSeries(spread)
        self.__spread = spread

    def getStandardizedSpread(self) -> pd.Series:
        return self.__standardizedSpread

    def setStandardizedSpread(self,
                              standardizedSpread: pd.Series) -> None:
        ErrorHandler.validateSpread(standardizedSpread)
        ErrorHandler.validateSeries(standardizedSpread)
        self.__standardizedSpread = standardizedSpread

    def getPair(self) -> Pair:
        return self.__pair

    def setPair(self, pair: Pair) -> None:
        ErrorHandler.validatePairName(pair.getPairName())
        self.__pair = pair

    def getEntryThreshold(self) -> int:
        return self.__entryThreshold

    def setEntryThreshold(self,
                          entryThreshold: int) -> None:
        ErrorHandler.validateInteger(entryThreshold)
        self.__entryThreshold = entryThreshold

    def getExitThreshold(self) -> pd.Series:
        return self.__exitThreshold

    def setExitThreshold(self,
                         exitThreshold: pd.Series) -> None:
        ErrorHandler.validateSeries(exitThreshold)
        self.__exitThreshold = exitThreshold

    def getOpenTrades(self) -> list[Trade]:
        return self.__openTrades

    def setOpenTrades(self,
                      openTrades: list[Trade]) -> None:
        ErrorHandler.validateTrades(openTrades)
        self.__openTrades = openTrades

    def getClosedTrades(self) -> list[Trade]:
        return self.__closedTrades

    def setClosedTrades(self,
                        closedTrades: list[Trade]) -> None:
        ErrorHandler.validateTrades(closedTrades)
        self.__closedTrades = closedTrades

    def addOpenTrade(self,
                     trade: Trade) -> None:
        ErrorHandler.validateTrade(trade)
        openTrades: list[Trade] = self.getOpenTrades()
        openTrades.append(trade)
        self.setOpenTrades(openTrades)

    def addClosedTrade(self,
                       trade: Trade) -> None:
        ErrorHandler.validateTrade(trade)
        closedTrades: list[Trade] = self.getClosedTrades()
        closedTrades.append(trade)
        self.setClosedTrades(closedTrades)

    def removeOpenTrade(self,
                        trade: Trade) -> None:
        openTrades: list[Trade] = self.getOpenTrades()
        for openTrade in openTrades:
            if trade == openTrade:
                openTrades.remove(openTrade)
        self.setOpenTrades(openTrades)

    def removeClosedTrade(self,
                          trade: Trade) -> None:
        closedTrades: list[Trade] = self.getClosedTrades()
        for closedTrade in closedTrades:
            if trade == closedTrade:
                closedTrades.remove(closedTrade)
        self.setClosedTrades(closedTrades)

    @staticmethod
    def calculateVolume(entryPrice1: float,
                        entryPrice2: float) -> (float, float):
        if entryPrice1 > entryPrice2:
            volume1: float = 1
            volume2: float = entryPrice1 / entryPrice2
        elif entryPrice1 < entryPrice2:
            volume1: float = entryPrice2 / entryPrice1
            volume2: float = 1
        else:
            volume1 = volume2 = 1

        return volume1, volume2

    def enterTrade(self,
                   symbol: str,
                   pairTradeDirection: int,
                   entryPrice: float,
                   entryTime,
                   direction: int,
                   volume: float) -> None:
        trade: Trade = Trade(symbol=symbol,
                             pairName=self.getPair().getPairName(),
                             pairTradeDirection=pairTradeDirection,
                             entryPrice=entryPrice,
                             entryTime=entryTime,
                             direction=direction,
                             volume=volume)
        self.addOpenTrade(trade)

    def exitTrade(self,
                  trade: Trade,
                  exitPrice: float,
                  exitTime) -> None:
        trade.setExitPrice(exitPrice)
        trade.setExitTime(exitTime)
        trade.calculateProfitLoss()
        self.removeOpenTrade(trade)
        self.addClosedTrade(trade)

    def enterPairsTrade(self,
                        date,
                        direction: int) -> None:
        pair: Pair = self.getPair()
        symbol1, symbol2 = pair.getPairName().split("_")
        data1: Data = pair.getInstrument1Data()
        data2: Data = pair.getInstrument2Data()

        entryPrice1: float = data1.getData().loc[date]
        entryPrice2: float = data2.getData().loc[date]
        entryTime = date
        if direction == 1:
            direction1: int = 1
            direction2: int = -1
        elif direction == -1:
            direction1: int = -1
            direction2: int = 1
        else:
            direction1: int = 0
            direction2: int = 0
            print("Invalid direction in Strategy")
        volume1, volume2 = self.calculateVolume(entryPrice1=entryPrice1,
                                                entryPrice2=entryPrice2)
        self.enterTrade(symbol=symbol1,
                        pairTradeDirection=direction,
                        entryPrice=entryPrice1,
                        entryTime=entryTime,
                        direction=direction1,
                        volume=volume1)
        self.enterTrade(symbol=symbol2,
                        pairTradeDirection=direction,
                        entryPrice=entryPrice2,
                        entryTime=entryTime,
                        direction=direction2,
                        volume=volume2)

    def exitPairsTrade(self,
                       trade1: Trade,
                       trade2: Trade,
                       exitPrice1: float,
                       exitPrice2: float,
                       exitTime) -> None:
        self.exitTrade(trade=trade1,
                       exitPrice=exitPrice1,
                       exitTime=exitTime)
        self.exitTrade(trade=trade2,
                       exitPrice=exitPrice2,
                       exitTime=exitTime)

    def findPairsTrade(self,
                       trade: Trade) -> Trade:
        openTrades: list[Trade] = self.getOpenTrades()
        for openTrade in openTrades:
            if trade.getEntryTime() == openTrade.getEntryTime() and \
                    trade.getSymbol() != openTrade.getSymbol() and \
                    trade.getDirection() != openTrade.getDirection() and \
                    trade.getPairName() == openTrade.getPairName() and \
                    trade.getPairTradeDirection() == openTrade.getPairTradeDirection():
                return openTrade

    def tradeFilter(self) -> bool:
        openTrades: list[Trade] = self.getOpenTrades()

        for openTrade in openTrades:
            if openTrade.getPairName() == self.getPair().getPairName():
                return False
        return True

    def findEntries(self,
                    date,
                    spread: pd.Series) -> None:
        entryThreshold: int = self.getEntryThreshold()
        tradeFilter: bool = self.tradeFilter()

        if spread <= -entryThreshold and tradeFilter:
            self.enterPairsTrade(date=date,
                                 direction=1)
        if spread >= entryThreshold and tradeFilter:
            self.enterPairsTrade(date=date,
                                 direction=-1)

    def findExits(self,
                  date,
                  spread: pd.Series) -> None:
        openTrades: list[Trade] = self.getOpenTrades()
        exitThreshold: pd.Series = self.getExitThreshold()

        pair: Pair = self.getPair()
        data1: Data = pair.getInstrument1Data()
        data2: Data = pair.getInstrument2Data()

        for openTrade in openTrades:
            longPosition: bool = openTrade.getPairTradeDirection() == 1
            shortPosition: bool = openTrade.getPairTradeDirection() == -1
            longExit: bool = spread >= exitThreshold[date]
            shortExit: bool = spread <= exitThreshold[date]


            long: bool = longPosition and longExit
            short: bool = shortPosition and shortExit
            if not (long or short):
                continue

            if data1.getSymbol() == openTrade.getSymbol():
                close1: float = data1.getData()[date]
                close2: float = data2.getData()[date]
            else:
                close1: float = data2.getData()[date]
                close2: float = data1.getData()[date]

            pairsTrade: Trade = self.findPairsTrade(openTrade)
            self.exitPairsTrade(trade1=openTrade,
                                trade2=pairsTrade,
                                exitPrice1=close1,
                                exitPrice2=close2,
                                exitTime=date)

    def findTrades(self) -> (list[Trade], list[Trade]):
        standardizedSpread: pd.Series = self.getStandardizedSpread()
        trainSetSpreads: int = self.getExitThreshold().index[0]
        for date, spread in standardizedSpread[trainSetSpreads:].items():
            self.findEntries(date,
                             spread)
            self.findExits(date,
                           spread)

    def getClosedTradesInfo(self) -> pd.DataFrame:
        return self.__closedTradesInfo

    def setClosedTradesInfo(self,
                            closedTradesInfo: pd.DataFrame) -> None:
        self.__closedTradesInfo = closedTradesInfo

    def createClosedTradesInfo(self) -> pd.DataFrame:
        closedTrades: list[Trade] = self.getClosedTrades()
        closedTradesInfo = {}
        for idx, trade in enumerate(closedTrades):
            closedTradesInfo[idx] = {
                "symbol": trade.getSymbol(),
                "pair": trade.getPairName(),
                "pairTradeDirection": trade.getPairTradeDirection(),
                "entryPrice": trade.getEntryPrice(),
                "exitPrice": trade.getExitPrice(),
                "entryTime": trade.getEntryTime(),
                "exitTime": trade.getExitTime(),
                "direction": trade.getDirection(),
                "volume": trade.getVolume(),
                "profitLoss": trade.getProfitLoss()
            }
        closedTradesInfo = pd.DataFrame.from_dict(closedTradesInfo, orient="index")

        try:
            closedTradesInfo["cumSum"] = closedTradesInfo["profitLoss"].cumsum()
        except KeyError:
            closedTradesInfo = pd.DataFrame()
            closedTradesInfo["cumSum"] = 0

        self.setClosedTradesInfo(closedTradesInfo)
        return closedTradesInfo

    def getTradesToday(self,
                       date,
                       spread: pd.Series) -> (str, str):
        result: list = ["", ""]
        entryThreshold: int = self.getEntryThreshold()
        exitThreshold: pd.Series = self.getExitThreshold()
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        date = str(date)
        date = spread.index[spread.index <= date].max()
        dateLastBar = spread.index[spread.index < date].max()

        if spread[date] <= -entryThreshold:
            result[0] = f"There is a long entry on {self.getPair().getPairName()} on the previous bar."
        elif spread[date] >= entryThreshold:
            result[0] = f"There is a short entry on {self.getPair().getPairName()} on the previous bar."
        else:
            result[0] = f"There is no entry on {self.getPair().getPairName()} on the previous bar."

        if spread[date] >= exitThreshold[date] and spread[dateLastBar] < exitThreshold[dateLastBar]:
            result[1] += f"There is a long exit on {self.getPair().getPairName()} on the previous bar."
        if spread[date] <= exitThreshold[date] and spread[dateLastBar] > exitThreshold[dateLastBar]:
            result[1] += f"There is a short exit on {self.getPair().getPairName()} on the previous bar."
        if result[1] == "":
            result[1] = f"There is no exit on {self.getPair().getPairName()} on the previous bar."

        return tuple(result)
