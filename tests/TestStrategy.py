import unittest
import datetime
import pandas as pd
from Pair import Pair
from Trade import Trade
from Strategy import Strategy
from DataSource import DataSource
from Data import Data
from Instrument import Instrument
from Model import Model


class TestStrategy(unittest.TestCase):
    def setUp(self):
        self.dataSource = DataSource("yahoo")
        self.instrument1 = Instrument("AAPL")
        self.instrument2 = Instrument("GOOG")
        self.startDate = datetime.datetime(2020, 1, 1, 0, 0, 0)
        self.endDate = datetime.datetime(2024, 1, 1, 0, 0, 0)
        self.timeframe = "1d"
        self.data1 = Data(self.dataSource, self.instrument1, self.startDate, self.endDate, self.timeframe)
        self.data2 = Data(self.dataSource, self.instrument2, self.startDate, self.endDate, self.timeframe)
        self.data1.downloadData()
        self.data2.downloadData()
        self.data1.setData(self.data1.cleanData())
        self.data2.setData(self.data2.cleanData())
        self.pair = Pair(self.data1, self.data2)
        self.pair.calculateSpread()
        self.pair.calculateStandardizedSpread(window=50)
        self.model = Model(pair=self.pair)
        self.model.predict(self.pair.getStandardizedSpread())
        fairMarketValue: pd.Series = self.model.getFairMarketValue()
        self.trade1 = Trade("AAPL",
                            "AAPL_GOOG",
                            1,
                            100,
                            datetime.datetime(2024, 3, 1, 0, 0, 0),
                            1,
                            1)
        self.trade2 = Trade("GOOG",
                            "AAPL_GOOG",
                            1,
                            200,
                            datetime.datetime(2024, 3, 1, 0, 0, 0),
                            -1,
                            .5)
        self.openTrades = [self.trade1, self.trade2]
        self.closedTrades = []
        self.strategy = Strategy(pair=self.pair,
                                 entryThreshold=2,
                                 exitThreshold=fairMarketValue)
        self.strategy.findTrades()

    def tearDown(self):
        del self.dataSource
        del self.instrument1
        del self.instrument2
        del self.startDate
        del self.endDate
        del self.timeframe
        del self.data1
        del self.data2
        del self.pair
        del self.model
        del self.strategy
        self.dataSource = None
        self.instrument1 = None
        self.instrument2 = None
        self.startDate = None
        self.endDate = None
        self.timeframe = None
        self.data1 = None
        self.data2 = None
        self.pair = None
        self.model = None
        self.strategy = None

    def testGettersSetters(self):
        self.setUp()
        self.strategy.setSpread(self.pair.getSpread())
        self.strategy.setStandardizedSpread(self.pair.getStandardizedSpread())
        self.assertTrue(self.strategy.getSpread().equals(self.pair.getSpread()))
        self.assertTrue(self.strategy.getStandardizedSpread().equals(self.pair.getStandardizedSpread()))
        with self.assertRaises(Exception):
            self.strategy.setSpread(5)
        with self.assertRaises(Exception):
            self.strategy.setStandardizedSpread(5)
        with self.assertRaises(Exception):
            self.strategy.setSpread("5")
        with self.assertRaises(Exception):
            self.strategy.setStandardizedSpread("5")
        with self.assertRaises(Exception):
            self.strategy.setSpread(None)
        with self.assertRaises(Exception):
            self.strategy.setStandardizedSpread(None)
        self.tearDown()

        self.setUp()
        self.strategy.setPair(self.pair)
        self.assertEqual(self.strategy.getPair(), self.pair)
        with self.assertRaises(Exception):
            self.strategy.setPair("pair")
        with self.assertRaises(Exception):
            self.strategy.setPair(None)
        self.tearDown()

        self.setUp()
        self.strategy.setEntryThreshold(3)
        self.assertEqual(self.strategy.getEntryThreshold(), 3)
        with self.assertRaises(Exception):
            self.strategy.setEntryThreshold("3")
        with self.assertRaises(Exception):
            self.strategy.setEntryThreshold(None)
        self.tearDown()

        self.setUp()
        self.strategy.setExitThreshold(self.model.getFairMarketValue())
        self.assertTrue((self.strategy.getExitThreshold().equals(self.model.getFairMarketValue())))
        with self.assertRaises(Exception):
            self.strategy.setExitThreshold(5)
        with self.assertRaises(Exception):
            self.strategy.setExitThreshold("5")
        with self.assertRaises(Exception):
            self.strategy.setExitThreshold(None)
        self.tearDown()

        self.setUp()
        self.strategy.setOpenTrades(self.openTrades)
        self.assertEqual(self.strategy.getOpenTrades(), self.openTrades)
        with self.assertRaises(Exception):
            self.strategy.setOpenTrades([1, 2])
        with self.assertRaises(Exception):
            self.strategy.setOpenTrades(["1", "2"])
        with self.assertRaises(Exception):
            self.strategy.setOpenTrades([None, None])
        self.tearDown()

        self.setUp()
        self.closedTrades = self.openTrades
        self.strategy.setClosedTrades(self.closedTrades)
        self.assertEqual(self.strategy.getClosedTrades(), self.openTrades)
        with self.assertRaises(Exception):
            self.strategy.setClosedTrades([1, 2])
        with self.assertRaises(Exception):
            self.strategy.setClosedTrades(["1", "2"])
        with self.assertRaises(Exception):
            self.strategy.setClosedTrades([None, None])
        self.tearDown()

    def testAddRemoveOpenClosedTrade(self):
        self.setUp()
        self.openTrades = []
        self.strategy.addOpenTrade(self.trade1)
        self.strategy.addOpenTrade(self.trade2)
        self.assertIn(self.trade1, self.strategy.getOpenTrades())
        self.assertIn(self.trade2, self.strategy.getOpenTrades())
        self.tearDown()

        self.setUp()
        self.strategy.addClosedTrade(self.trade1)
        self.strategy.addClosedTrade(self.trade2)
        self.assertIn(self.trade1, self.strategy.getClosedTrades())
        self.assertIn(self.trade2, self.strategy.getClosedTrades())
        self.tearDown()

        self.setUp()
        self.strategy.removeOpenTrade(self.trade1)
        self.assertNotIn(self.trade1, self.strategy.getOpenTrades())
        self.tearDown()

        self.setUp()
        self.strategy.removeClosedTrade(self.trade2)
        self.assertNotIn(self.trade2, self.strategy.getClosedTrades())
        self.strategy.addClosedTrade(self.trade2)
        self.assertIn(self.trade2, self.strategy.getClosedTrades())
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.strategy.addOpenTrade(1)
        with self.assertRaises(Exception):
            self.strategy.addOpenTrade("1")
        with self.assertRaises(Exception):
            self.strategy.addOpenTrade(None)
        with self.assertRaises(Exception):
            self.strategy.addClosedTrade(1)
        with self.assertRaises(Exception):
            self.strategy.addClosedTrade("1")
        with self.assertRaises(Exception):
            self.strategy.addClosedTrade(None)
        self.tearDown()

        self.setUp()
        try:
            self.strategy.enterTrade("AAPL",
                                 1,
                                 100,
                                 datetime.datetime(2023, 3, 1, 0, 0, 0),
                                 1,
                                 1)
        except:
            self.fail("enterTrade()")
        with self.assertRaises(Exception):
            self.strategy.enterTrade(None,None,None,None,None,None)
        self.tearDown()

        self.setUp()
        date = self.strategy.getSpread().index[0]
        self.strategy.enterPairsTrade(date, 1)
        with self.assertRaises(Exception):
            self.strategy.enterPairsTrade(date, 2)
        with self.assertRaises(Exception):
            self.strategy.enterPairsTrade(None, 1)
        self.tearDown()


if __name__ == '__main__':
    unittest.main()
