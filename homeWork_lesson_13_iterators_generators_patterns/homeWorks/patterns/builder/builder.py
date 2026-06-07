from homeWorks.patterns.builder.pizza import Pizza
from typing import Any


class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()

    def set_size(self, size: Any):
        self.pizza.size = size
        return self

    def set_cheese(self, cheese: Any):
        self.pizza.cheese = cheese
        return self

    def set_pepperoni(self, pepperoni: Any):
        self.pizza.pepperoni = pepperoni
        return self

    def set_mushrooms(self, mushrooms: Any):
        self.pizza.mushrooms = mushrooms
        return self

    def set_onions(self, onions: Any):
        self.pizza.onions = onions
        return self

    def set_beacon(self, bacon: Any):
        self.pizza.bacon = bacon
        return self

    def build(self) -> Pizza:
        return self.pizza
