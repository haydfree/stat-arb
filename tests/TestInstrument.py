import unittest
import random
import string
from Instrument import Instrument


class TestInstrument(unittest.TestCase):
    def setUp(self):
        self.instrument = Instrument(symbol="AAPL")

    def tearDown(self):
        del self.instrument
        self.instrument = None

    def testGetterSetterSymbolCorrectValues(self):
        self.setUp()
        self.assertEqual("AAPL", self.instrument.getSymbol())
        self.tearDown()

        self.setUp()
        self.instrument.setSymbol("MSFT")
        self.assertEqual("MSFT", self.instrument.getSymbol())
        self.tearDown()

        self.setUp()
        self.instrument.setSymbol("SPY")
        self.assertEqual("SPY", self.instrument.getSymbol())
        self.tearDown()

    def testGetterSetterSymbolIncorrectValues(self):
        self.setUp()
        with self.assertRaises(Exception):
            self.instrument.setSymbol(1)
        self.assertEqual("AAPL", self.instrument.getSymbol())
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.instrument.setSymbol(0)
        self.assertEqual("AAPL", self.instrument.getSymbol())
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.instrument.setSymbol(False)
        self.assertEqual("AAPL", self.instrument.getSymbol())
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.instrument.setSymbol(69)
        self.assertEqual("AAPL", self.instrument.getSymbol())
        self.tearDown()

        self.setUp()
        with self.assertRaises(Exception):
            self.instrument.setSymbol("POOP")
        self.assertEqual("AAPL", self.instrument.getSymbol())
        self.tearDown()

    def testGetterSetterSymbolNullValues(self):
        self.setUp()
        with self.assertRaises(Exception):
            self.instrument.setSymbol(None)
        self.assertEqual("AAPL", self.instrument.getSymbol())
        self.tearDown()

    def testGetterSetterSymbolExtremeValues(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        randomString = ''.join(random.choice(characters) for _ in range(100))
        self.setUp()
        with self.assertRaises(Exception):
            self.instrument.setSymbol(randomString)
            print(self.instrument.getSymbol())
        self.assertEqual("AAPL", self.instrument.getSymbol())
        self.tearDown()


if __name__ == '__main__':
    unittest.main()
