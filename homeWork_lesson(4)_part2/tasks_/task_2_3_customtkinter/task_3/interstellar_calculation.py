from math import pi


def calculate_planets_year(*, orbital_radius: float, orbital_velocity: float) -> float:
    length_of_a_year = 2 * orbital_radius * pi / orbital_velocity

    return length_of_a_year
