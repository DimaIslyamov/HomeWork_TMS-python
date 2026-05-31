from typing import Self


class Bus:
    def __init__(
            self,
            speed: float = 0,
            maximum_seating_capacity: int = 50,
            maximum_speed: float = 120,
    ):

        self._speed = speed
        self._maximum_seating_capacity = maximum_seating_capacity
        self._maximum_speed = maximum_speed

        self._passenger_list: list[str] = []
        self._free_seats: bool = True
        self._seats_in_bus: dict[str, int] = {}

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def maximum_seating_capacity(self) -> int:
        return self._maximum_seating_capacity

    @property
    def maximum_speed(self) -> float:
        return self._maximum_speed

    @property
    def passenger_list(self) -> list[str]:
        return self._passenger_list.copy()

    @property
    def free_seats(self) -> bool:
        return self._free_seats

    @property
    def seats_in_bus(self) -> dict[str, int]:
        return self._seats_in_bus.copy()

    # ==== метод флага ====
    def _update_free_seats(self) -> None:
        self._free_seats = (
                len(self._passenger_list)
                < self._maximum_seating_capacity)

    # ==== получение свободных мест ====
    def _get_free_seat(self) -> int:
        occupied_seats = set(self._seats_in_bus.values())

        for seat in range(1, self._maximum_seating_capacity + 1):
            if seat not in occupied_seats:
                return seat

        raise ValueError("Свободных мест нет")

    # ==== посадка и высадка одного пассажира ====
    def add_passenger(self, passenger: str) -> None:
        if passenger in self._passenger_list:
            raise ValueError("Такой пассажир уже в автобусе")

        seat = self._get_free_seat()

        self._passenger_list.append(passenger)
        self._seats_in_bus[passenger] = seat
        self._update_free_seats()

    def remove_passenger(self, passenger: str) -> None:
        if passenger not in self._passenger_list:
            raise ValueError("Такого пассажира в списке нет.")

        self._passenger_list.remove(passenger)
        del self._seats_in_bus[passenger]
        self._update_free_seats()

    # ==== посадка и высадка нескольких пассажиров ====
    def add_passengers(self, passengers: list[str]) -> None:
        for passenger in passengers:
            self.add_passenger(passenger)

    def remove_passengers(self, passengers: list[str]) -> None:
        for passenger in passengers:
            self.remove_passenger(passenger)

    # ==== увеличение и уменьшение скорости на заданное значение ====
    def increase_speed(self, value: float) -> None:
        if value < 0:
            raise ValueError("Скорость нельзя увеличивать на отрицательное число")

        self._speed = min(self._speed + value, self._maximum_speed)

    def decrease_speed(self, value: float) -> None:
        if value < 0:
            raise ValueError("Скорость нельзя уменьшать на отрицательное число")

        self._speed = max(self._speed - value, 0)

    # ==== операции in, += и - =====
    def __contains__(self, item) -> bool:
        return item in self._passenger_list

    def __iadd__(self, other: str) -> Self:
        self.add_passenger(other)
        return self

    def __isub__(self, other: str) -> Self:
        self.remove_passenger(other)
        return self
