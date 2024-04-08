import unittest
import datetime
import pandas as pd
from Pair import Pair
from DataSource import DataSource
from Data import Data
from Instrument import Instrument


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.dataSource = DataSource("yahoo")
        self.instrument1 = Instrument("AAPL")
        self.instrument2 = Instrument("GOOG")
        self.startDate = datetime.datetime(2023, 1, 1, 0, 0, 0)
        self.endDate = datetime.datetime(2024, 1, 1, 0, 0, 0)
        self.timeframe = "1d"
        self.data1 = Data(self.dataSource, self.instrument1, self.startDate, self.endDate, self.timeframe)
        self.data2 = Data(self.dataSource, self.instrument2, self.startDate, self.endDate, self.timeframe)
        self.data1.downloadData()
        self.data2.downloadData()
        self.data1.setData(self.data1.cleanData())
        self.data2.setData(self.data2.cleanData())
        self.pair = Pair(self.data1, self.data2)

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
        self.dataSource = None
        self.instrument1 = None
        self.instrument2 = None
        self.startDate = None
        self.endDate = None
        self.timeframe = None
        self.data1 = None
        self.data2 = None
        self.pair = None

    def testGetSetInstrument(self):
        self.setUp()
        try:
            self.pair.setInstrument1(Instrument("MSFT"))
            self.pair.setInstrument2(Instrument("SPY"))
        except:
            self.fail("set instrument")
        self.tearDown()

        self.setUp()
        self.assertTrue(self.pair.getInstrument1().getSymbol() == "AAPL")
        self.assertTrue(self.pair.getInstrument2().getSymbol() == "GOOG")
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.pair.setInstrument1(Instrument("poop"))
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.pair.setInstrument2(Instrument(69))
        self.tearDown()

        self.setUp()
        self.assertTrue(self.pair.getInstrument1Data() == self.data1)
        self.assertTrue(self.pair.getInstrument2Data() == self.data2)
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.pair.setInstrument1Data("poop")
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.pair.setInstrument2Data(69)
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.pair.setInstrument1Data(None)
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.pair.setInstrument2Data(None)
        self.tearDown()

    def testGetSetPairName(self):
        self.setUp()
        self.assertTrue(self.pair.getPairName() == f"{self.instrument1.getSymbol()}_{self.instrument2.getSymbol()}")
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.pair.setPairName("poop")
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.pair.setPairName(69)
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.pair.setPairName(None)
        self.tearDown()

        self.setUp()
        self.pair.setPairName("GOOG_AAPL")
        self.assertTrue(self.pair.getPairName() == "GOOG_AAPL")
        self.tearDown()

    def testSpread(self):
        self.setUp()
        try:
            self.pair.calculateSpread()
        except:
            self.fail("Spread normal")
        self.tearDown()

        self.setUp()
        series = pd.Series(range(0, 150))
        self.pair.setSpread(series)
        self.assertTrue(self.pair.getSpread().equals(series))
        self.tearDown()

        self.setUp()
        self.data1.setData(pd.DataFrame(range(0, 150)))
        self.data2.setData(pd.DataFrame(range(150, 0, -1)))
        try:
            self.pair.calculateSpread()
        except:
            self.fail("Spread with range")
        self.tearDown()

        self.setUp()
        try:
            self.pair.calculateSpread()
            self.pair.calculateStandardizedSpread(window=50)
        except:
            self.fail("Spread + standard spread")
        self.tearDown()




if __name__ == '__main__':
    unittest.main()
