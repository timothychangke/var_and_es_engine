from var_engine.core.identifiers import Currency


class VarEngineError(Exception):
    """
    Base exception for all internal domain errors raised by the engine. These are the
    errors that the callers should catch in order to handle risk related failures
    """


class CurrencyMismatchError(VarEngineError):
    """
    Raised when arithematic operations are performed on different currencies
    """

    def __init__(self, left_currency: Currency, right_currency: Currency):
        super().__init__(
            f"Currencies {left_currency} and {right_currency} are incompatible"
        )
        # State is preserved
        self.left_currency = left_currency
        self.right_currency = right_currency
