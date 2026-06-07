from homeWorks.patterns.strategy.operations import Operation


class Calculator:
    def __init__(self, strategy: Operation | None = None) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: Operation) -> None:
        self._strategy = strategy

    def calculate(self, value_one: int | float,
                  value_two: int | float) -> int | float:

        if self._strategy is None:
            raise ValueError('Calculator has not been initialized')

        return self._strategy.execute(value_one, value_two)

