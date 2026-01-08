"""Animated starfield background for the UI."""

import curses
import random
import time

from .rendering import get_palette, safe_addch


def init_starfield(height, width, density=0.01):
    """Create a list of stars with positions, speed, and twinkle state."""
    max_cells = max(1, (height - 2) * (width - 2))
    count = max(12, int(max_cells * density))
    stars = []
    for _ in range(count):
        stars.append(_make_star(height, width))
    return {"stars": stars, "last": time.monotonic()}


def _make_star(height, width):
    star = getattr(curses, "ACS_BULLET", ".")
    return {
        "y": random.uniform(1, max(1, height - 2)),
        "x": random.randint(1, max(1, width - 2)),
        "speed": random.uniform(0.2, 0.8),
        "char": star,
        "twinkle": random.uniform(0.8, 1.6),
        "next": time.monotonic() + random.uniform(0.8, 1.6),
    }


def update_starfield(state, height, width):
    """Update star positions and twinkle state based on elapsed time."""
    now = time.monotonic()
    delta = max(0.0, now - state.get("last", now))
    state["last"] = now

    for star in state["stars"]:
        star["y"] += star["speed"] * delta
        if star["y"] >= height - 1:
            star.update(_make_star(height, width))
            star["y"] = 1
        if now >= star["next"]:
            star["char"] = getattr(curses, "ACS_BULLET", ".")
            star["next"] = now + star["twinkle"]


def render_starfield(stdscr, height, width, state):
    """Render stars behind the playfield."""
    palette = get_palette()
    for star in state["stars"]:
        y = int(star["y"])
        x = int(star["x"])
        if 0 < y < height - 1 and 0 < x < width - 1:
            safe_addch(stdscr, y, x, star["char"], palette["stars"])
