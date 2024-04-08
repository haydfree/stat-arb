import unittest
import datetime

import numpy as np
import pandas as pd
from DataSource import DataSource
from Instrument import Instrument
from Data import Data


class TestData(unittest.TestCase):
    def setUp(self):
        self.dataSource = DataSource(source="yahoo")
        self.instrument = Instrument(symbol="AAPL")
        self.startDate = datetime.datetime(2023, 1, 1)
        self.endDate = datetime.datetime(2024, 1, 1)
        self.timeframe = "1d"
        self.data = Data(self.dataSource, self.instrument, self.startDate, self.endDate, self.timeframe)

    def tearDown(self):
        del self.dataSource, self.instrument, self.startDate, self.endDate, self.timeframe
        self.dataSource = None
        self.instrument = None
        self.startDate = None
        self.endDate = None
        self.timeframe = None

    # Test getters and setters for DataSource
    def testGetterSetterDataSourceCorrect(self):
        self.assertEqual(self.data.getDataSource(), self.dataSource)

    def testGetterSetterDataSourceIncorrect(self):
        with self.assertRaises(Exception):
            self.data.setDataSource("IncorrectDataSource")

    def testGetterSetterDataSourceNull(self):
        with self.assertRaises(Exception):
            self.data.setDataSource(None)

    # Test getters and setters for Instrument
    def testGetterSetterInstrumentCorrect(self):
        self.assertEqual(self.data.getInstrument(), self.instrument)

    def testGetterSetterInstrumentIncorrect(self):
        with self.assertRaises(Exception):
            self.data.setInstrument("IncorrectInstrument")

    def testGetterSetterInstrumentNull(self):
        with self.assertRaises(Exception):
            self.data.setInstrument(None)

    # Test getters and setters for Data
    def testGetterSetterDataCorrect(self):
        data = self.data.downloadData()
        self.assertTrue(self.data.getData().equals(data))

    def testGetterSetterDataIncorrect(self):
        with self.assertRaises(Exception):
            self.data.setData("IncorrectData")

    def testGetterSetterDataNull(self):
        with self.assertRaises(Exception):
            self.data.setData(None)

    def testGetterSetterDataExtreme(self):
        self.setUp()
        self.data.setStartDate(datetime.datetime(1900,1,1,0,0,0))
        data = self.data.downloadData()
        self.data.setData(data)
        self.assertTrue(self.data.getData().equals(data))

    # Test getSymbol and setSymbol
    def testGetterSetterSymbolCorrect(self):
        self.assertEqual(self.data.getSymbol(), "AAPL")

    def testGetterSetterSymbolIncorrect(self):
        with self.assertRaises(Exception):
            self.data.setSymbol("IncorrectSymbol")

    def testGetterSetterSymbolNull(self):
        with self.assertRaises(Exception):
            self.data.setSymbol(None)

    # Test getStartDate and setStartDate
    def testGetterSetterStartDateCorrect(self):
        self.assertEqual(self.data.getStartDate(), self.startDate)

    def testGetterSetterStartDateIncorrect(self):
        with self.assertRaises(Exception):
            self.data.setStartDate("IncorrectStartDate")

    def testGetterSetterStartDateNull(self):
        with self.assertRaises(Exception):
            self.data.setStartDate(None)

    def testGetterSetterStartDateExtreme(self):
        startDate = datetime.datetime(1900, 1, 1)
        self.data.setStartDate(startDate)
        self.assertEqual(self.data.getStartDate(), startDate)

    # Test getEndDate and setEndDate
    def testGetterSetterEndDateCorrect(self):
        self.assertEqual(self.data.getEndDate(), self.endDate)

    def testGetterSetterEndDateIncorrect(self):
        with self.assertRaises(Exception):
            self.data.setEndDate("IncorrectEndDate")

    def testGetterSetterEndDateNull(self):
        with self.assertRaises(Exception):
            self.data.setEndDate(None)

    def testGetterSetterEndDateExtreme(self):
        endDate = datetime.datetime(2050, 1, 1)
        self.data.setEndDate(endDate)
        self.assertEqual(self.data.getEndDate(), endDate)

    # Test getTimeframe and setTimeframe
    def testGetterSetterTimeframeCorrect(self):
        self.assertEqual(self.data.getTimeframe(), "1d")

    def testGetterSetterTimeframeIncorrect(self):
        with self.assertRaises(Exception):
            self.data.setTimeframe("IncorrectTimeframe")

    def testGetterSetterTimeframeNull(self):
        with self.assertRaises(Exception):
            self.data.setTimeframe(None)

    # Test downloadData and cleanData
    def testDownloadDataCorrect(self):
        self.setUp()
        data = self.data.downloadData()
        self.assertIsInstance(data, pd.DataFrame)
        self.tearDown()

    def testDownloadDataIncorrect(self):
        pass

    def testDownloadDataNull(self):
        pass

    def testDownloadDataExtreme(self):
        pass

    def testCleanDataCorrect(self):
        self.setUp()
        data = self.data.downloadData()
        cleanedData = self.data.cleanData()
        self.assertIsInstance(cleanedData, pd.Series)
        self.assertFalse(np.isnan(cleanedData).any())
        self.tearDown()

    def testCleanDataIncorrect(self):
        pass

    def testCleanDataNull(self):
        pass

    def testCleanDataExtreme(self):
        pass


if __name__ == '__main__':
    unittest.main()
