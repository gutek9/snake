"""Game state helpers for Snake."""

import random
from collections import deque


def make_initial_snake(height, width):
    """Create the starting snake centered in the terminal."""
    start_y = height // 2
    start_x = width // 2
    snake = deque(
        [
            (start_y, start_x),
            (start_y, start_x - 1),
            (start_y, start_x - 2),
        ]
    )
    return snake, {pos for pos in snake}


def place_food(height, width, snake):
    """Place food in a random unoccupied cell, or return None if full."""
    max_cells = (height - 2) * (width - 2)
    if len(snake) >= max_cells:
        return None
    while True:
        y = random.randint(1, height - 2)
        x = random.randint(1, width - 2)
        if (y, x) not in snake:
            return (y, x)
