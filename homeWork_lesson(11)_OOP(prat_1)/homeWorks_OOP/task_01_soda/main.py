class Soda:
    def __init__(self, taste=None):
        self.taste = taste


    def __str__(self):
        if self.taste:
            return f'У вас газировка с {self.taste} вкусом'
        return "У вас обычная газировка"


if __name__ == "__main__":
    soda_1 = Soda("клубничным")
    print(soda_1)

    soda_2 = Soda()
    print(soda_2)
