import time
from fp_homeWork.utils import run_time


def calculate_room_area(room: dict[str, float]) -> float | int:
    return room["length"] * room["width"]


@run_time
def calculate_flat_area(rooms: list[dict[str, float]]) -> float | int:
    time.sleep(1.5)
    return sum(map(calculate_room_area, rooms))
