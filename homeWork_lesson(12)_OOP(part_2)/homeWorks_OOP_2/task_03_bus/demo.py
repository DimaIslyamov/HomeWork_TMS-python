from homeWorks_OOP_2.task_03_bus.bus import Bus


def show_bus_info(buus: Bus) -> None:
    print("=== Состояние автобуса ===")
    print(f"Скорость: {buus.speed}")
    print(f"Максимальная скорость: {buus.maximum_speed}")
    print(f"Максимум мест: {buus.maximum_seating_capacity}")
    print(f"Есть свободные места: {buus.free_seats}")
    print(f"Пассажиры: {buus.passenger_list}")
    print(f"Места в автобусе: {buus.seats_in_bus}")
    print()


bus = Bus(maximum_seating_capacity=3, maximum_speed=100)

print("Автобус создан")
show_bus_info(bus)


print("Посадка одного пассажира:")
bus.add_passenger("Ivanov")
show_bus_info(bus)


print("Посадка нескольких пассажиров:")
bus.add_passengers(["Petrov", "Sidorov"])
show_bus_info(bus)


print("Проверка оператора in:")
print("Ivanov" in bus)
print("Smirnov" in bus)
print()


print("Попытка посадить пассажира, когда мест уже нет:")
try:
    bus.add_passenger("Smirnov")
except ValueError as error:
    print(f"Ошибка: {error}")
print()


print("Высадка одного пассажира:")
bus.remove_passenger("Petrov")
show_bus_info(bus)


print("Посадка через оператор +=:")
bus += "Smirnov"
show_bus_info(bus)


print("Высадка через оператор -=:")
bus -= "Ivanov"
show_bus_info(bus)


print("Проверка, что освободившееся место используется снова:")
bus += "Kozlov"
show_bus_info(bus)


print("Увеличение скорости:")
bus.increase_speed(40)
show_bus_info(bus)


print("Попытка увеличить скорость выше максимальной:")
bus.increase_speed(1000)
show_bus_info(bus)


print("Уменьшение скорости:")
bus.decrease_speed(30)
show_bus_info(bus)


print("Попытка уменьшить скорость ниже нуля:")
bus.decrease_speed(1000)
show_bus_info(bus)


print("Попытка увеличить скорость на отрицательное число:")
try:
    bus.increase_speed(-10)
except ValueError as error:
    print(f"Ошибка: {error}")
print()


print("Попытка уменьшить скорость на отрицательное число:")
try:
    bus.decrease_speed(-10)
except ValueError as error:
    print(f"Ошибка: {error}")
print()


print("Попытка посадить пассажира повторно:")
try:
    bus.add_passenger("Smirnov")
except ValueError as error:
    print(f"Ошибка: {error}")
print()


print("Попытка высадить пассажира, которого нет:")
try:
    bus.remove_passenger("Unknown")
except ValueError as error:
    print(f"Ошибка: {error}")
print()


print("Финальное состояние автобуса:")
show_bus_info(bus)
