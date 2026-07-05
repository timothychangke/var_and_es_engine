from __future__ import annotations

from dataclasses import dataclass

from ..exceptions import CurrencyMismatchError
from .identifiers import Currency


@dataclass(frozen=True)
class Money:
    amount: float
    currency: Currency

    @classmethod
    # Explicitly to override the default start state of sum()
    def zero(cls, currency: Currency) -> Money:
        return cls(amount=0, currency=currency)

    # __add__() is called first. Only if NotImplemented if returned is __radd__() called
    # other type can be object here as validation is done within the function
    def __add__(self, other: object) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise CurrencyMismatchError(self.currency, other.currency)
        return Money(amount=other.amount + self.amount, currency=self.currency)

    def __radd__(self, other: object) -> Money:
        # Zero catch is needed as python's sum() implicitly calls 0 + ... when sum() is called
        if isinstance(other, int) and other == 0:
            return self
        return self.__add__(other)

    def __sub__(self, other: object) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise CurrencyMismatchError(self.currency, other.currency)
        return Money(amount=self.amount - other.amount, currency=self.currency)

    def __neg__(self) -> Money:
        return Money(amount=-self.amount, currency=self.currency)

    # Money is multiplied with a scalar
    def __mul__(self, scalar: object) -> Money:
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Money(amount=self.amount * scalar, currency=self.currency)

    def __rmul__(self, other: object) -> Money:
        if isinstance(other, int) and other == 1:
            return self
        return self.__mul__(other)
