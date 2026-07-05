from dataclasses import dataclass
from enum import StrEnum


class Currency(StrEnum):
    USD = "USD"
    EUR = "EUR"
    SGD = "SGD"
    GBP = "GBP"
    CNY = "CNY"
    JPY = "JPY"
    CHF = "CHF"

    # Class method that normalises currency. _missing_ is the fallback method that gets called when you instantiate a python enum by value but Python cannot find the exact match
    @classmethod
    def _missing_(cls, value: object) -> Currency | None:
        if isinstance(value, str):
            normalised = value.strip().upper()
            # Prevents indefinite recursion
            if normalised != value:
                try:
                    return cls(normalised)
                except ValueError:
                    # If string is still invalid, Enum will throw a ValueError.
                    # Catching it and returning None will let Python raise this final error.
                    return None
        return None


class RiskFactorKind(StrEnum):
    EQ = "EQ"  # Equity Spot
    FX = "FX"  # FX Rate
    IV = "IV"  # Implied Volatility
    IR = "IR"  # Interest / Discount rate


@dataclass(frozen=True)
class RiskFactorId:
    kind: RiskFactorKind
    symbol: str
    tenor: str | None = None

    def __post_init__(self) -> None:
        symbol = self.symbol.strip().upper()
        if not symbol:
            raise ValueError("RiskFactorId requires a non-empty symbol")
        object.__setattr__(self, "symbol", symbol)

        tenor = self.tenor.strip().upper() if self.tenor is not None else None
        object.__setattr__(self, "tenor", tenor or None)

    def __str__(self) -> str:
        return (
            f"{self.kind}:{self.symbol}:{self.tenor}"
            if self.tenor
            else f"{self.kind}:{self.symbol}"
        )
