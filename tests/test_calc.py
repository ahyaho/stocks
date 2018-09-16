import mock
import pytest

from datetime import datetime

from stocks.calc import (STOCKS, STOCK_ALE, STOCK_GIN, STOCK_SELL_INDICATOR,
                         flush_trade_logs, logger, geometric_mean)


@pytest.fixture()
def stock_ale():
    return STOCKS[STOCK_ALE]


@pytest.fixture()
def stock_gin():
    return STOCKS[STOCK_GIN]


@pytest.fixture()
def price():
    return 1000


@pytest.fixture()
def flush_trades():
    flush_trade_logs()


class TestStock:
    @pytest.mark.parametrize('stock_symbol,expected_dividend_yield', [
        (STOCK_ALE, 0.023),
        (STOCK_GIN, 0.2),
    ])
    def test_get_dividend_yield(self, stock_ale, stock_gin, price,
                                stock_symbol, expected_dividend_yield):
        stock = stock_ale if stock_symbol == STOCK_ALE else stock_gin
        assert stock.get_dividend_yield(price) == expected_dividend_yield

    @pytest.mark.parametrize('stock_symbol,expected_ratio', [
        (STOCK_ALE, 43.47826086956522),
        (STOCK_GIN, 125.0),
    ])
    def test_get_dividend_yield(self, stock_ale, stock_gin, price,
                                stock_symbol, expected_ratio):
        stock = stock_ale if stock_symbol == STOCK_ALE else stock_gin
        assert stock.get_pe_ratio(price) == expected_ratio

    def test_get_volume_weighted_price(self, stock_gin, flush_trades):
        stock = stock_gin
        stock.record_trade(trade_price=100, quantity_of_shares=20,
                           sell_or_by_indicator=STOCK_SELL_INDICATOR)
        stock.record_trade(trade_price=120, quantity_of_shares=12,
                           sell_or_by_indicator=STOCK_SELL_INDICATOR)
        assert stock.get_volume_weighted_price() == 107.5

    def test_record_trade(self, stock_gin, stock_ale, flush_trades):
        dt = datetime(2018, 9, 17, 1, 28, 46, 35774)
        with mock.patch('stocks.calc.datetime_now', return_value=dt):
            stock_gin.record_trade(trade_price=100, quantity_of_shares=20,
                                   sell_or_by_indicator=STOCK_SELL_INDICATOR)
            stock_ale.record_trade(trade_price=120, quantity_of_shares=12,
                                   sell_or_by_indicator=STOCK_SELL_INDICATOR)
        assert logger.read('GIN') == [
            {
                'symbol': 'GIN',
                'quantity': 20,
                'indicator': 'sell',
                'price': 100,
                'timestamp': dt
            },
        ]
        assert logger.read('ALE') == [
            {
                'symbol': 'ALE',
                'quantity': 12,
                'indicator': 'sell',
                'price': 120,
                'timestamp': dt
            },
        ]


def test_geometric_mean(stock_gin, stock_ale, flush_trades):
    stock_gin.record_trade(trade_price=100, quantity_of_shares=20,
                           sell_or_by_indicator=STOCK_SELL_INDICATOR)
    stock_ale.record_trade(trade_price=120, quantity_of_shares=12,
                           sell_or_by_indicator=STOCK_SELL_INDICATOR)
    assert geometric_mean() == 109.54451150103323

