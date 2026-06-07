from homeWorks.patterns.builder.builder import PizzaBuilder
from homeWorks.patterns.builder.pizza import Pizza


class PizzaDirector:
    @staticmethod
    def make_pizza(builder: PizzaBuilder) -> Pizza:
        return (
            builder
            .set_size('Medium')
            .set_cheese(True)
            .set_pepperoni(False)
            .set_mushrooms(True)
            .set_onions(True)
            .set_beacon(True)
            .build()
        )
