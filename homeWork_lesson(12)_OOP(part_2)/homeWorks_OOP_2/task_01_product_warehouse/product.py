class Product:
    def __init__(self, name, shop_name, price_zloty) -> None:
        self._name = name
        self._shop_name = shop_name
        self._price_zloty  = price_zloty

    def __str__(self) -> str:
        return (f"Товар : {self._name}\n"
                f"Магазин : {self._shop_name}\n"
                f"Цена : {self._price_zloty} zl"
                f"\n")

    def __add__(self, other: "Product") -> float:
        return self._price_zloty + other.price_zloty

    @property
    def name(self) -> str:
        return self._name

    @property
    def shop_name(self) -> str:
        return self._shop_name

    @property
    def price_zloty(self) -> float:
        return self._price_zloty
