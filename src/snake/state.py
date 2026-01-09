"""Game state helpers for Snake."""

import random
from collections import deque


def make_initial_snake(height, width, bounds=None):
    """Create the starting snake centered in the playable bounds."""
    if bounds is None:
        min_y, max_y, min_x, max_x = 1, height - 2, 1, width - 2
    else:
        min_y, max_y, min_x, max_x = bounds
    start_y = (min_y + max_y) // 2
    start_x = (min_x + max_x) // 2
    if max_x - min_x >= 2:
        start_x = max(min_x + 2, min(start_x, max_x))
    else:
        start_x = max_x
    snake = deque(
        [
            (start_y, start_x),
            (start_y, start_x - 1),
            (start_y, start_x - 2),
        ]
    )
    return snake, {pos for pos in snake}


def place_food(
    height,
    width,
    snake,
    min_y=1,
    max_y=None,
    min_x=1,
    max_x=None,
):
    """Place food in a random unoccupied cell, or return None if full."""
    max_y = height - 2 if max_y is None else max_y
    max_x = width - 2 if max_x is None else max_x
    if max_y < min_y or max_x < min_x:
        return None
    max_cells = (max_y - min_y + 1) * (max_x - min_x + 1)
    if len(snake) >= max_cells:
        return None
    while True:
        y = random.randint(min_y, max_y)
        x = random.randint(min_x, max_x)
        if (y, x) not in snake:
            return (y, x)
