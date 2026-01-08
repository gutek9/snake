"""Main menu rendering and input handling."""

import curses

from .rendering import draw_border, get_palette, safe_addstr

_OPTIONS = ["New Game", "High Scores", "Exit"]


def _render_menu(stdscr, height, width, selected):
    palette = get_palette()
    stdscr.erase()
    draw_border(stdscr, height, width)

    title = "Terminal Snake"
    safe_addstr(
        stdscr,
        2,
        max(1, width // 2 - len(title) // 2),
        title,
        palette["hud"],
    )

    start_y = height // 2 - len(_OPTIONS) // 2
    for idx, label in enumerate(_OPTIONS):
        attr = palette["hud"]
        if idx == selected:
            attr |= curses.A_REVERSE
        safe_addstr(
            stdscr,
            start_y + idx,
            max(1, width // 2 - len(label) // 2),
            label,
            attr,
        )

    footer = "Use arrows or W/S, Enter to select"
    safe_addstr(
        stdscr,
        height - 2,
        max(1, width // 2 - len(footer) // 2),
        footer,
        palette["hud"],
    )

    stdscr.refresh()


def menu_loop(stdscr, height, width):
    """Return the selected menu option string."""
    selected = 0
    stdscr.nodelay(False)

    while True:
        _render_menu(stdscr, height, width, selected)
        key = stdscr.getch()
        if key in (curses.KEY_UP, ord("w"), ord("W")):
            selected = (selected - 1) % len(_OPTIONS)
        elif key in (curses.KEY_DOWN, ord("s"), ord("S")):
            selected = (selected + 1) % len(_OPTIONS)
        elif key in (curses.KEY_ENTER, 10, 13):
            return _OPTIONS[selected]
        elif key in (ord("q"), ord("Q"), 27):
            return "Exit"
        elif key == curses.KEY_RESIZE:
            height, width = stdscr.getmaxyx()
