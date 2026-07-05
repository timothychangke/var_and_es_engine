from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Collection, Iterator
from dataclasses import dataclass
from typing import assert_never

from .instruments import Equity, EuropeanOption, FXSpot, Instrument


@dataclass(frozen=True)
class Position:
    instrument: Instrument
    # Supports fractional notionals
    quantity: float


def _underlier_key(underlier: Equity | FXSpot) -> str:
    match underlier:
        case Equity(symbol=symbol, currency=currency):
            return f"0|{symbol}|{currency}"
        case FXSpot(base_currency=base_currency, quote_currency=quote_currency):
            return f"1|{base_currency}|{quote_currency}"
        case _:
            assert_never(underlier)


def _sorted_key(instrument: Instrument) -> tuple[int, str, str, float, str]:
    match instrument:
        case Equity(symbol=symbol, currency=currency):
            return (0, symbol, currency.value, 0.0, "")
        case FXSpot(base_currency=base_currency, quote_currency=quote_currency):
            return (1, base_currency.value, quote_currency.value, 0.0, "")
        case EuropeanOption(
            option_type=option_type, strike=strike, expiry=expiry, underlying=underlying
        ):
            return (
                2,
                _underlier_key(underlying),
                option_type.value,
                strike,
                expiry.isoformat(),
            )
        case _:
            assert_never(instrument)


@dataclass(frozen=True)
class Portfolio(Collection[Position]):
    # Indicates a variable length tuple where every element is a Position
    positions: tuple[Position, ...]

    def __post_init__(self) -> None:
        """
        Nets position quantities and sorts them
        """
        grouped: dict[Instrument, list[float]] = defaultdict(list)
        for position in self.positions:
            grouped[position.instrument].append(position.quantity)

        netted_positions = (
            Position(instrument=instrument, quantity=math.fsum(quantities))
            for instrument, quantities in grouped.items()
        )
        # Positions with 0.0 quantities are removed
        sorted_positions = tuple(
            sorted(
                (position for position in netted_positions if position.quantity != 0.0),
                key=lambda p: _sorted_key(p.instrument),
            )
        )

        object.__setattr__(self, "positions", sorted_positions)

    def __len__(self) -> int:
        return len(self.positions)

    def __iter__(self) -> Iterator[Position]:
        return iter(self.positions)

    def __contains__(self, item: object) -> bool:
        return item in self.positions

    def holds(self, instrument: Instrument) -> bool:
        """
        Checks for instrument level membership
        """
        return any(p.instrument == instrument for p in self.positions)

    def __str__(self) -> str:
        if not self.positions:
            return "Portfolio(empty)"
        else:
            position_str = ", ".join(str(p) for p in self.positions)
            return f"Portfolio({len(self.positions)} positions = [{position_str}])"
