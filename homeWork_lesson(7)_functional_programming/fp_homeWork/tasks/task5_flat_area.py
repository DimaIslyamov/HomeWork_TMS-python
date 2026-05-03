import time
from functools import reduce
from fp_homeWork.utils import run_time


def calculate_room_area(room: dict) -> float | int:
    return room["length"] * room["width"]

@run_time
def calculate_flat_area(rooms: list[dict]) -> float | int:
    time.sleep(1.5)
    area = map(calculate_room_area, rooms)
    return reduce(lambda acc, x: acc + x, area, 0)
