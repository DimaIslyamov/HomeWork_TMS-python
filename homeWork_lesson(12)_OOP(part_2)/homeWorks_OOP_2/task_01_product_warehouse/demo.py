from homeWorks_OOP_2.task_01_product_warehouse.product import Product
from homeWorks_OOP_2.task_01_product_warehouse.warehouse import Warehouse


product1 = Product("Milk", "Auchan", 3.19)
product2 = Product("Bread", "Lidl", 2.49)
product3 = Product("Apple", "Biedronka", 1.99)
product4 = Product("Banana", "Biedronka", 4.47)
product5 = Product("Susi", "Lidl", 15.29)

warehouse = Warehouse(
    products=[product1,
              product2,
              product3,
              product4,
              product5]
)

search_index = warehouse.get_by_index(0)
search_index_two = warehouse.get_by_index(3)
search_index_three = warehouse.get_by_index(6)

print(f"Товар со склада 1 \n{search_index}\n"
      f"Товар со склада 2 \n{search_index_two}\n"
      f"Товар со склада 3 \n{search_index_three}")
print()

found_product = warehouse.get_by_name("Milk")
found_product_two = warehouse.get_by_name("Bread")

print(f"Товар по имени 1 \n{found_product}\n"
      f"Товар по имени 2 \n{found_product_two}\n")
print()

print("Sorted methods")
# warehouse.sort_by_name()
# warehouse.show_all()

# warehouse.sort_by_price()
# warehouse.show_all()
#
warehouse.sort_by_shop()
warehouse.show_all()
