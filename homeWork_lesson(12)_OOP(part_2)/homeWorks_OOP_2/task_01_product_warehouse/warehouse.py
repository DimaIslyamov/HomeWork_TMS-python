from homeWorks_OOP_2.task_01_product_warehouse.product import Product


class Warehouse:
    def __init__(self, products: list[Product] ) -> None:
        self._products = products

    def add_product(self, product: Product) -> None:
        self._products.append(product)

    def get_by_index(self, index: int) -> Product | str:
        if 0 <= index < len(self._products):
            return self._products[index]

        return "Продукта с таким индексом нет"

    def get_by_name(self, name: str) -> Product | None:
        for product in self._products:
            if product.name == name:
                return product

        return None

    def sort_by_name(self) -> None:
        self._products.sort(key=lambda product: product.name)

    def sort_by_shop(self) -> None:
        self._products.sort(key=lambda product: product.shop_name)

    def sort_by_price(self) -> None:
        self._products.sort(key=lambda product: product.price_zloty)

    def show_all(self) -> None:
        for product in self._products:
            print(product)
