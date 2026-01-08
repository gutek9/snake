"""Keyboard input handling for Snake."""

import curses

# Direction vectors are (dy, dx) in row/column terms.
_DIRECTION_MAP = {
    ord("w"): (-1, 0),
    ord("s"): (1, 0),
    ord("a"): (0, -1),
    ord("d"): (0, 1),
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
}


def next_direction(key, current):
    """Translate a key press into a direction, guarding against reversals."""
    proposed = _DIRECTION_MAP.get(key, current)
    if (proposed[0] == -current[0] and proposed[1] == -current[1]):
        return current
    return proposed
