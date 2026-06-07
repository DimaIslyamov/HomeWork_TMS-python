from homeWorks.patterns.builder.builder import PizzaBuilder
from homeWorks.patterns.builder.director import PizzaDirector
from homeWorks.patterns.factory.factory import AnimalFactory
from homeWorks.patterns.strategy.calculator import Calculator
from homeWorks.patterns.strategy.operations import (
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation,
)


def main() -> None:

    # === Pizza Builder ===
    builder = PizzaBuilder()
    pizza = PizzaDirector.make_pizza(builder=builder)
    print(pizza)

    # === Factory Method Animals ===
    animal_dog = AnimalFactory.create_animal(name="Bob", animal_type='dog')
    print(animal_dog.speak())

    animal_cat = AnimalFactory.create_animal(name="Liz", animal_type='cat')
    print(animal_cat.speak())

    # === Strategy Calculator ===
    calculator = Calculator()

    calculator.set_strategy(AddOperation())
    print(f"10 + 5 = {calculator.calculate(10, 5)}")

    calculator.set_strategy(SubtractOperation())
    print(f"10 - 5 = {calculator.calculate(10, 5)}")

    calculator.set_strategy(MultiplyOperation())
    print(f"10 * 5 = {calculator.calculate(10, 5)}")

    calculator.set_strategy(DivideOperation())
    print(f"10 / 5 = {calculator.calculate(10, 5)}")


if __name__ == '__main__':
    main()
