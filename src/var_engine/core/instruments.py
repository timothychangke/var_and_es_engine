from dataclasses import dataclass
from datetime import date
from enum import StrEnum

from .identifiers import Currency


# Mixin of str and enum is need in this case so that encoders can natively match, validate and serialise the enum values directly without transforming the string into a OptionType Instance.
class OptionType(StrEnum):
    # name = value
    CALL = "call"
    PUT = "put"


@dataclass(frozen=True)
class Equity:
    symbol: str
    currency: Currency

    def __post_init__(self) -> None:
        symbol = self.symbol.strip().upper()
        if not symbol:
            raise ValueError("An equity requires a corresponding symbol")
        object.__setattr__(self, "symbol", symbol)


@dataclass(frozen=True)
class FXSpot:
    base_currency: Currency
    quote_currency: Currency

    def __post_init__(self) -> None:
        if self.base_currency == self.quote_currency:
            raise ValueError("Both base and the quote curency cannot be the same")


type Underlying = Equity | FXSpot


@dataclass(frozen=True)
class EuropeanOption:
    option_type: OptionType
    strike: float
    expiry: date
    underlying: Underlying

    def __post_init__(self) -> None:
        if self.strike <= 0.0:
            raise ValueError("Strike price cannot be less than zero")


type Instrument = Equity | EuropeanOption | FXSpot
