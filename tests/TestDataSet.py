import unittest
import datetime
from DataSet import DataSet
from Data import Data
from Instrument import Instrument
from DataSource import DataSource


class TestDataSet(unittest.TestCase):
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
        self.dataset = DataSet(data1=self.data1, data2=self.data2)

    def tearDown(self):
        del self.dataSource
        del self.instrument1
        del self.instrument2
        del self.startDate
        del self.endDate
        del self.timeframe
        del self.data1
        del self.data2
        del self.dataset
        self.dataSource = None
        self.instrument1 = None
        self.instrument2 = None
        self.startDate = None
        self.endDate = None
        self.timeframe = None
        self.data1 = None
        self.data2 = None
        self.dataset = None

    def testGetterSetterDataCorrect(self):
        self.setUp()
        self.instrument1.setData(self.dataset.getData("AAPL").getData())
        self.instrument2.setData(self.dataset.getData("GOOG").getData())
        self.assertTrue(self.dataset.getData("AAPL").getData().equals(self.instrument1.getData()))
        self.assertTrue(self.dataset.getData("GOOG").getData().equals(self.instrument2.getData()))
        self.tearDown()
        self.setUp()
        try:
            self.dataset.setData("AAPL", self.data1)
            self.dataset.setData("GOOG", self.data2)
        except Exception:
            self.fail("Exception")

    def testGetterSetterDataIncorrect(self):
        self.setUp()
        with self.assertRaises(Exception):
            self.dataset.getData("poop")
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.dataset.getData(1)
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.dataset.setData("poop", self.data1)
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.dataset.setData("AAPL", 1)
        self.tearDown()

    def testGetterSetterDataNull(self):
        self.setUp()
        with self.assertRaises(Exception):
            self.dataset.setData(None, self.data1)
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.dataset.setData("AAPL", None)
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.dataset.setData(None, None)
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.dataset.getData(None)
        self.tearDown()

    def testGetterSetterDataSetCorrect(self):
        self.setUp()
        self.dataset.setDataSet([self.data1, self.data2])
        self.assertEqual(self.dataset.getDataSet(), [self.data1, self.data2])
        self.tearDown()

    def testGetterSetterDataSetIncorrect(self):
        self.setUp()
        self.data1 = "poop"
        self.data2 = 69
        with self.assertRaises(Exception):
            self.dataset.setDataSet([self.data1, self.data2])
        self.tearDown()

        self.setUp()
        self.data2 = list[self.data2]
        with self.assertRaises(Exception):
            self.dataset.setDataSet([self.data1, self.data2])
        self.tearDown()

    def testGetterSetterDataSetNull(self):
        self.setUp()
        with self.assertRaises(Exception):
            self.dataset.setData("poop", None)
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.dataset.getData(None)
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.dataset.setData(None, 69)
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.dataset.setDataSet(None)
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.dataset.getDataSet(None)
        self.tearDown()

    def testGetterSetterCleanCorrect(self):
        self.setUp()
        try:
            self.dataset.cleanDataSet()
        except Exception as e:
            self.fail("CleanDataSet")
        self.tearDown()

        self.setUp()
        data1 = self.data2
        data2 = self.data1
        self.data1.setData(data1.getData())
        self.data2.setData(data2.getData())
        self.tearDown()


if __name__ == '__main__':
    unittest.main()
