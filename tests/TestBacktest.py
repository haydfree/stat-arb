import unittest
from Backtest import Backtest


class TestBacktest(unittest.TestCase):
    def setUp(self):
        self.backtest = Backtest()
        self.backtest