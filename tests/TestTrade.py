import unittest
from datetime import datetime
from Trade import Trade


class TestTrade(unittest.TestCase):

    def setUp(self):
        self.trade1 = Trade(symbol='AAPL',
                            pairName='AAPL_MSFT',
                            pairTradeDirection=1,
                            entryPrice=150.0,
                            entryTime=datetime(2023, 5, 15, 9, 30),
                            direction=1,
                            volume=1.0)
        self.trade2 = Trade(symbol='MSFT',
                            pairName='AAPL_MSFT',
                            pairTradeDirection=1,
                            entryPrice=200.0,
                            entryTime=datetime(2023, 5, 15, 9, 30),
                            direction=-1,
                            volume=1.0)

    def tearDown(self):
        del self.trade1
        del self.trade2
        self.trade1 = None
        self.trade2 = None

    def testGetterSetters(self):
        self.setUp()
        self.assertEqual(self.trade1.getSymbol(), "AAPL")
        self.assertEqual(self.trade2.getSymbol(), "MSFT")
        self.trade1.setSymbol("MSFT")
        self.assertEqual(self.trade1.getSymbol(), "MSFT")
        with self.assertRaises(Exception):
            self.trade1.setSymbol(1)
        with self.assertRaises(Exception):
            self.trade1.setSymbol("1")
        with self.assertRaises(Exception):
            self.trade1.setSymbol(None)
        self.tearDown()

        self.setUp()
        self.assertEqual(self.trade1.getPairName(), "AAPL_MSFT")
        self.assertEqual(self.trade2.getPairName(), "AAPL_MSFT")
        self.trade1.setPairName("MSFT_AAPL")
        self.assertEqual(self.trade1.getPairName(), "MSFT_AAPL")
        with self.assertRaises(Exception):
            self.trade1.setPairName(1)
        with self.assertRaises(Exception):
            self.trade1.setPairName("1")
        with self.assertRaises(Exception):
            self.trade1.setPairName(None)
        self.tearDown()

        self.setUp()
        self.assertEqual(self.trade1.getPairTradeDirection(), 1)
        self.assertEqual(self.trade2.getPairTradeDirection(), 1)
        self.trade1.setPairTradeDirection(-1)
        self.assertEqual(self.trade1.getPairTradeDirection(), -1)
        with self.assertRaises(Exception):
            self.trade1.setPairTradeDirection(69)
        with self.assertRaises(Exception):
            self.trade1.setPairTradeDirection("69")
        with self.assertRaises(Exception):
            self.trade1.setPairTradeDirection(None)
        self.tearDown()

        self.setUp()
        self.assertEqual(self.trade1.getEntryPrice(), 150.0)
        self.assertEqual(self.trade2.getEntryPrice(), 200.0)
        self.trade1.setEntryPrice(100.0)
        self.assertEqual(self.trade1.getEntryPrice(), 100.0)
        with self.assertRaises(Exception):
            self.trade1.setEntryPrice(-100.0)
        with self.assertRaises(Exception):
            self.trade1.setEntryPrice("69")
        with self.assertRaises(Exception):
            self.trade1.setEntryPrice(None)
        self.tearDown()

        self.setUp()
        self.assertEqual(self.trade1.getEntryTime(), datetime(2023, 5, 15, 9, 30))
        self.assertEqual(self.trade2.getEntryTime(), datetime(2023, 5, 15, 9, 30))
        self.trade1.setEntryTime(datetime(2024, 1, 3, 9, 30))
        self.assertEqual(self.trade1.getEntryTime(), datetime(2024, 1, 3, 9, 30))
        with self.assertRaises(Exception):
            self.trade1.setEntryTime(-100.0)
        with self.assertRaises(Exception):
            self.trade1.setEntryTime("69")
        with self.assertRaises(Exception):
            self.trade1.setEntryTime(None)
        self.tearDown()

        self.setUp()
        self.assertEqual(self.trade1.getDirection(), 1)
        self.assertEqual(self.trade2.getDirection(), -1)
        self.trade1.setDirection(-1)
        self.assertEqual(self.trade1.getDirection(), -1)
        with self.assertRaises(Exception):
            self.trade1.setDirection(-100.0)
        with self.assertRaises(Exception):
            self.trade1.setDirection("69")
        with self.assertRaises(Exception):
            self.trade1.setDirection(None)
        self.tearDown()

        self.setUp()
        self.assertEqual(self.trade1.getVolume(), 1.0)
        self.assertEqual(self.trade2.getVolume(), 1.0)
        self.trade1.setVolume(2.0)
        self.assertEqual(self.trade1.getVolume(), 2.0)
        with self.assertRaises(Exception):
            self.trade1.setVolume(-100.0)
        with self.assertRaises(Exception):
            self.trade1.setVolume("69")
        with self.assertRaises(Exception):
            self.trade1.setVolume(None)
        self.tearDown()


if __name__ == '__main__':
    unittest.main()
