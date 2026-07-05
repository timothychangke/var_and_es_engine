import random
from datetime import date

import pytest

from var_engine.core.identifiers import Currency
from var_engine.core.instruments import Equity, EuropeanOption, FXSpot, OptionType
from var_engine.core.money import Money
from var_engine.core.portfolio import Portfolio, Position
from var_engine.exceptions import CurrencyMismatchError

TEST_CASES = [(10.0, 5.0), (-100.0, 100.0), (0.00, 0.00), (1.23456, 9.87654)]


@pytest.mark.parametrize("a, b", TEST_CASES)
def test_money_addition_commutes(a: float, b: float) -> None:
    m1 = Money(amount=a, currency=Currency.USD)
    m2 = Money(amount=b, currency=Currency.USD)

    assert m1 + m2 == m2 + m1


def test_currency_mismatch_error() -> None:
    m1 = Money(amount=40, currency=Currency.USD)
    m2 = Money(amount=50, currency=Currency.CHF)

    with pytest.raises(CurrencyMismatchError):
        _ = m1 + m2


PERMUTATION_CASES = [
    [10.0, 20.0, 30.0, -10.0],
    [1e16, 1.0, -1e16],
    [0.0001, -0.0001, 0.0002],
]


@pytest.mark.parametrize("quantities", PERMUTATION_CASES)
def test_portfolio_permutation(quantities: list[float]) -> None:
    instrument = Equity(symbol="AAPL", currency=Currency.USD)
    original_positions = [
        Position(instrument=instrument, quantity=q) for q in quantities
    ]

    shuffled_positions = original_positions.copy()
    random.shuffle(shuffled_positions)

    original_portfolio = Portfolio(positions=tuple(original_positions))
    shuffled_portfolio = Portfolio(positions=tuple(shuffled_positions))

    assert original_portfolio.positions == shuffled_portfolio.positions


def test_dod_integration_portfolio_netting() -> None:
    # Arrange
    aapl = Equity(symbol="AAPL", currency=Currency.USD)
    eurusd = FXSpot(base_currency=Currency.EUR, quote_currency=Currency.USD)
    aapl_call = EuropeanOption(
        option_type=OptionType.CALL,
        strike=150.0,
        expiry=date(2026, 12, 18),
        underlying=aapl,
    )

    raw_trades = (
        Position(aapl, 100.0),
        Position(aapl, -50.0),
        Position(eurusd, 1_000_000.0),
        Position(eurusd, 500_000.0),
        Position(aapl_call, 10.0),
        Position(aapl_call, 10.0),
        Position(Equity("MSFT", Currency.USD), 200.0),
        Position(Equity("TSLA", Currency.USD), -10.0),
        Position(Equity("IBM", Currency.USD), 50.0),
        Position(Equity("IBM", Currency.USD), -50.0),
    )

    # Act
    book = Portfolio(raw_trades)

    # Assert
    assert len(book) == 5

    ibm = Equity(symbol="IBM", currency=Currency.USD)
    assert not book.holds(ibm)

    # Next is used as a generator expression extracting only one specific item in a collection
    aapl_position = next(p for p in book if p.instrument == aapl)
    assert aapl_position.quantity == 50.00

    eurusd_position = next(p for p in book if p.instrument == eurusd)
    assert eurusd_position.quantity == 1_500_000.0

    option_position = next(p for p in book if p.instrument == aapl_call)
    assert option_position.quantity == 20.0


HASH_TEST_CASES = [10.0, 0.0, -100.5, 1e9]


@pytest.mark.parametrize("amount", HASH_TEST_CASES)
def test_value_object_hash_equality(amount: float) -> None:
    m1 = Money(amount=amount, currency=Currency.USD)
    m2 = Money(amount=amount, currency=Currency.USD)

    assert m1 == m2
    assert hash(m1) == hash(m2)
