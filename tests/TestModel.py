import unittest
from sklearn import linear_model
import pandas as pd
import datetime
from Model import Model
from Pair import Pair
from DataSource import DataSource
from Data import Data
from Instrument import Instrument


class TestModel(unittest.TestCase):
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
        self.model = Model(self.pair)
        self.model.predict(self.pair.getStandardizedSpread())

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

    def testSetFairMarketValue(self):
        self.setUp()
        FMV = self.model.getFairMarketValue()
        self.assertEqual(self.model.getFairMarketValue().tolist(), FMV.tolist())
        self.tearDown()

    def testSetModel(self):
        self.setUp()
        model = self.model.getModel()
        self.model.setModel(model)
        self.assertEqual(self.model.getModel(), model)
        self.tearDown()

    def testSetPair(self):
        self.setUp()
        pair = self.pair
        self.model.setPair(pair)
        self.assertEqual(self.model.getPair(), pair)
        self.tearDown()

    def testPredict(self):
        self.setUp()
        model = self.model.getModel()
        self.model.setModel(model)
        try:
            self.model.predict(self.pair.getStandardizedSpread())
        except:
            self.fail("model predict")
        self.tearDown()


if __name__ == '__main__':
    unittest.main()
