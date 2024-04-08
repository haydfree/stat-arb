import unittest
from datetime import datetime
import pandas as pd
from DataSource import DataSource


class TestDataSource(unittest.TestCase):

    def setUp(self):
        self.dataSource = DataSource(source="yahoo")

    def tearDown(self):
        del self.dataSource
        self.dataSource = None

    def testGetterSetterCorrectValues(self):
        self.setUp()
        self.dataSource.setSource("yahoo")
        self.assertEqual("yahoo", self.dataSource.getSource())
        self.tearDown()

    def testGetterSetterIncorrectValues(self):
        self.setUp()
        self.dataSource.setSource("yaho")
        self.assertEqual("yaho", self.dataSource.getSource())
        self.tearDown()

        self.setUp()
        self.dataSource.setSource(1)
        self.assertEqual(1, self.dataSource.getSource())
        self.tearDown()

        self.setUp()
        self.dataSource.setSource("1")
        self.assertEqual("1", self.dataSource.getSource())
        self.tearDown()

        self.setUp()
        self.dataSource.setSource(False)
        self.assertEqual(False, self.dataSource.getSource())
        self.tearDown()

        self.setUp()
        self.dataSource.setSource(0)
        self.assertEqual(0, self.dataSource.getSource())
        self.tearDown()

        self.setUp()
        self.dataSource.setSource(True)
        self.assertEqual(True, self.dataSource.getSource())
        self.tearDown()

    def testGetterSetterNullValues(self):
        self.setUp()
        self.dataSource.setSource(None)
        self.assertEqual(None, self.dataSource.getSource())
        self.tearDown()

    def testGetterSetterExtremeValues(self):
        self.setUp()
        self.dataSource.setSource(float("inf"))
        self.assertEqual(float("inf"), self.dataSource.getSource())
        self.tearDown()

    def testDownloadDataCorrectValues(self):
        symbol = "AAPL"
        startDate = datetime(2022, 1, 1)
        endDate = datetime(2022, 1, 10)
        timeframe = "1d"
        result = self.dataSource.downloadData(symbol, startDate, endDate, timeframe)
        self.assertFalse(result.empty)

    def testDownloadDataIncorrectValues(self):
        symbol = "INVALID_SYMBOL"
        startDate = 1
        endDate = True
        timeframe = 69
        with self.assertRaises(Exception):
            self.dataSource.downloadData(symbol, startDate, endDate, timeframe)

    def testDownloadDataNullValues(self):
        symbol = "AAPL"
        startDate = None
        endDate = None
        timeframe = "1d"
        with self.assertRaises(Exception):
            self.dataSource.downloadData(symbol, startDate, endDate, timeframe)

    def testDownloadDataExtremeValues(self):
        symbol = "AAPL"
        startDate = datetime.min
        endDate = datetime.max
        timeframe = "1m"
        with self.assertRaises(Exception):
            self.dataSource.downloadData(symbol, startDate, endDate, timeframe)

if __name__ == "__main__":
    unittest.main()
