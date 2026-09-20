import math
import re

from constants import MAX_CHARGE
from constants import MAX_ELEVATION


def parse_position(pos):
    """
     Converts:
    F4 3:7 into: (5.3, 3.7)
    """
    pattern = r"^([A-T])(\d{1,2})\s+(\d):(\d)$"

    match = re.match(pattern, pos.strip().upper())

    if not match:
        raise ValueError(
            f"Invalid coordinate format: {pos}"
        )

    letter = match.group(1)
    grid_y = int(match.group(2))
    mini_x = int(match.group(3))
    mini_y = int(match.group(4))

    x = (ord(letter) - ord("A")) + mini_x / 10
    y = (grid_y - 1) + mini_y / 10

    return x, y


def calculate_distance(gun, target):

    dx = target[0] - gun[0]
    dy = target[1] - gun[1]

    return round(
        math.sqrt(dx * dx + dy * dy),
        2
    )


def calculate_bearing(gun, target):

    dx = target[0] - gun[0]
    dy = target[1] - gun[1]

    bearing = math.degrees(
        math.atan2(dx, dy)
    )

    if bearing < 0:
        bearing += 360

    return round(bearing)


def get_valid_charges(distance):

    solutions = []

    for charge in range(1, MAX_CHARGE + 1):

        elevation = distance * (12 / charge)

        if elevation <= MAX_ELEVATION:

            solutions.append((charge, round(elevation, 1)))

    return solutions