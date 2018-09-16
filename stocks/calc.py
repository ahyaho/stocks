"""
Stock Symbol    Type        Last Dividend   Fixed Dividend  Par Value
TEA             Common      0               NA              100
POP             Common      8               NA              100
ALE             Common      23              NA              60
GIN             Preferred   8               2%              100
JOE             Common      13              NA              250
"""

from collections import defaultdict
from functools import reduce
from datetime import datetime

STOCK_TYPE_COMMON = 'Common'
STOCK_TYPE_PREFERRED = 'Preferred'

STOCK_SELL_INDICATOR = 'sell'
STOCK_BUY_INDICATOR = 'buy'

STOCK_TEA = 'TEA'
STOCK_POP = 'POP'
STOCK_ALE = 'ALE'
STOCK_GIN = 'GIN'
STOCK_JOE = 'JOE'


def datetime_now():
    """
    Just for easier mocking in tests
    :return:
    """
    return datetime.now()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class TradeLogger(metaclass=Singleton):
    def __init__(self):
        self._log = defaultdict(list)

    def write(self, key, value):
        self._log[key].append(value)

    def read(self, key):
        return self._log[key]

    def readall(self):
        return self._log

    def flush(self):
        self._log = defaultdict(list)


logger = TradeLogger()


class Stock:
    def __init__(self, *, stock_symbol, stock_type,
                 last_dividend, fixed_dividend, par_value):
        self.stock_symbol = stock_symbol
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value

    def get_dividend_yield(self, market_price):
        """
        Given a market price as input, calculates the dividend yield.

        :param market_price:
        :return:
        """
        if self.stock_type == STOCK_TYPE_COMMON:
            return self.last_dividend / market_price
        return self.fixed_dividend * self.par_value / market_price

    def get_pe_ratio(self, market_price):
        """
        Given a market price as input, calculates the P/E Ratio

        :return:
        """
        return market_price / self.last_dividend

    def get_volume_weighted_price(self):
        """
        Calculates Volume Weighted Stock Price based on trades in past 15 minutes.
        :return:
        """
        numerator = sum([r['price'] * r['quantity'] for r in logger.read(self.stock_symbol)])
        denominator = sum([r['quantity'] for r in logger.read(self.stock_symbol)])
        return numerator / denominator

    def record_trade(self, *, trade_price, quantity_of_shares, sell_or_by_indicator):
        """
        Records a trade, with timestamp, quantity of shares, buy or sell indicator and trade price.

        :return:
        """
        assert sell_or_by_indicator in [STOCK_SELL_INDICATOR, STOCK_BUY_INDICATOR]
        data = {
            'symbol': self.stock_symbol,
            'quantity': quantity_of_shares,
            'indicator': sell_or_by_indicator,
            'price': trade_price,
            'timestamp': datetime_now(),
        }
        logger.write(self.stock_symbol, data)


STOCKS = {
    STOCK_TEA: Stock(stock_symbol=STOCK_TEA, stock_type=STOCK_TYPE_COMMON,
                     last_dividend=0, fixed_dividend=None, par_value=100),
    STOCK_POP: Stock(stock_symbol=STOCK_POP, stock_type=STOCK_TYPE_COMMON,
                     last_dividend=8, fixed_dividend=None, par_value=100),
    STOCK_ALE: Stock(stock_symbol=STOCK_ALE, stock_type=STOCK_TYPE_COMMON,
                     last_dividend=23, fixed_dividend=None, par_value=60),
    STOCK_GIN: Stock(stock_symbol=STOCK_GIN, stock_type=STOCK_TYPE_PREFERRED,
                     last_dividend=8, fixed_dividend=2, par_value=100),
    STOCK_JOE: Stock(stock_symbol=STOCK_JOE, stock_type=STOCK_TYPE_COMMON,
                     last_dividend=13, fixed_dividend=None, par_value=250),
}


def flush_trade_logs():
    logger.flush()


def geometric_mean():
    """
    Calculates the GBCE All Share Index using the geometric mean of prices for all stocks.
    :return:
    """
    all_prices = []
    for trade_logs in logger.readall().values():
        all_prices.extend([trade_log['price'] for trade_log in trade_logs])
    return reduce(lambda x, y: x * y, all_prices) ** (1.0 / len(all_prices))
