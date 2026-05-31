class Bus:
    def __init__(
            self,
            speed: float,
            maximum_seating_capacity: int,
            maximum_speed: float,
            passenger_list: list[str],
            free_seats: bool,
            seats_in_bus: dict[str, int],):

        self._speed = speed
        self._maximum_seating_capacity = maximum_seating_capacity
        self._maximum_speed = maximum_speed
        self._passenger_list = passenger_list
        self._free_seats = free_seats
        self._seats_in_bus = seats_in_bus

    # ==== Методы ====
    # ● посадка и высадка одного или нескольких пассажиров
    def add_passenger(self):
        pass

    def remove_passenger(self):
        pass

    def add_passengers(self, passengers: list[str]):
        pass

    def remove_passengers(self, passengers: list[str]):
        pass


    # ● увеличение и уменьшение скорости на заданное значение
    def increase_speed(self):
        pass

    def decrease_speed(self):
        pass


    # ● операции in, += и -= (посадка и высадка пассажира по фамилии)
    # __contains__()
    # __iadd__()
    # __isub__()