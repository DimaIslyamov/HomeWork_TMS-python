from homeWorks.patterns.factory.animal import Animal
from homeWorks.patterns.factory.animals.cat import Cat
from homeWorks.patterns.factory.animals.dog import Dog


class AnimalFactory:
    @staticmethod
    def create_animal(name: str, animal_type: str):
        if animal_type == "dog":
            return Dog(name)
        elif animal_type == "cat":
            return Cat(name)
        else:
            return ValueError(f"Unknown animal type: {animal_type}")
