"""Curses drawing helpers used by the game loop."""

import curses


def safe_addch(stdscr, y, x, ch):
    """Best-effort draw for single characters; ignore tiny terminal errors."""
    try:
        stdscr.addch(y, x, ch)
    except curses.error:
        pass


def safe_addstr(stdscr, y, x, text):
    """Best-effort draw for strings; ignore tiny terminal errors."""
    try:
        stdscr.addstr(y, x, text)
    except curses.error:
        pass


def draw_border(stdscr, height, width):
    """Draw a rectangular border around the playable area."""
    max_y = height - 1
    max_x = width - 1
    for x in range(width):
        safe_addch(stdscr, 0, x, "#")
        safe_addch(stdscr, max_y, x, "#")
    for y in range(height):
        safe_addch(stdscr, y, 0, "#")
        safe_addch(stdscr, y, max_x, "#")


def render(stdscr, height, width, snake, food, score):
    """Render the current game state to the screen."""
    stdscr.erase()
    draw_border(stdscr, height, width)
    safe_addstr(stdscr, 0, 2, f" Score: {score} ")

    if food is not None:
        fy, fx = food
        safe_addch(stdscr, fy, fx, "*")

    head = snake[0]
    safe_addch(stdscr, head[0], head[1], "@")
    for y, x in list(snake)[1:]:
        safe_addch(stdscr, y, x, "o")

    stdscr.refresh()


def render_center_message(stdscr, height, width, lines):
    """Render a centered multi-line message (game over, win, etc.)."""
    start_y = height // 2
    for offset, line in enumerate(lines):
        start_x = max(1, width // 2 - len(line) // 2)
        safe_addstr(stdscr, start_y + offset, start_x, line)
    stdscr.refresh()
