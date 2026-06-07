from homeWorks.patterns.factory.animal import Animal


class Cat(Animal):
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return f"Кот {self.name} говорит: Ммрр-мяу"
