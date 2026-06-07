from abc import ABC, abstractmethod


class Operation(ABC):
    @abstractmethod
    def execute(self, value_one: int | float,
                value_two: int | float) -> int | float:
        pass


class AddOperation(Operation):
    def execute(self, value_one: int | float,
                value_two: int | float) -> int | float:
        return value_one + value_two


class SubtractOperation(Operation):
    def execute(self, value_one: int | float,
                value_two: int | float) -> int | float:
        return value_one - value_two


class MultiplyOperation(Operation):
    def execute(self, value_one: int | float,
                value_two: int | float) -> int | float:
        return value_one * value_two


class DivideOperation(Operation):
    def execute(self, value_one: int | float,
                value_two: int | float) -> int | float:
        if value_two != 0:
            return value_one / value_two
        else:
            raise ZeroDivisionError("Division by zero")
