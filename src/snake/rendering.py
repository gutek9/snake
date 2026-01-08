"""Curses drawing helpers used by the game loop."""

import curses


# Color palette and sprite set are initialized once from the game loop.
_PALETTE = {
    "border": 0,
    "food": 0,
    "head": 0,
    "body": 0,
    "hud": 0,
    "message": 0,
}
_SPRITES = {
    "hline": "-",
    "vline": "|",
    "ul": "+",
    "ur": "+",
    "ll": "+",
    "lr": "+",
    "food": "*",
    "head": "@",
    "body": "o",
}


def init_colors(stdscr):
    """Initialize color pairs for a bright arcade look."""
    if not curses.has_colors():
        return _PALETTE
    curses.start_color()
    try:
        curses.use_default_colors()
    except curses.error:
        pass

    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_BLUE, -1)
    curses.init_pair(5, curses.COLOR_WHITE, -1)
    curses.init_pair(6, curses.COLOR_RED, -1)

    _PALETTE.update(
        {
            "border": curses.color_pair(1),
            "food": curses.color_pair(2),
            "head": curses.color_pair(3) | curses.A_BOLD,
            "body": curses.color_pair(4),
            "hud": curses.color_pair(5) | curses.A_BOLD,
            "message": curses.color_pair(6) | curses.A_BOLD,
        }
    )
    return _PALETTE


def init_sprites():
    """Prefer curses graphics characters; fall back to ASCII."""
    _SPRITES.update(
        {
            "hline": getattr(curses, "ACS_HLINE", "-"),
            "vline": getattr(curses, "ACS_VLINE", "|"),
            "ul": getattr(curses, "ACS_ULCORNER", "+"),
            "ur": getattr(curses, "ACS_URCORNER", "+"),
            "ll": getattr(curses, "ACS_LLCORNER", "+"),
            "lr": getattr(curses, "ACS_LRCORNER", "+"),
            "food": getattr(curses, "ACS_DIAMOND", "*"),
            "head": getattr(curses, "ACS_CKBOARD", "@"),
            "body": getattr(curses, "ACS_BLOCK", "o"),
        }
    )
    return _SPRITES


def init_style(stdscr):
    """Initialize colors and sprites for a more graphical look."""
    init_colors(stdscr)
    init_sprites()


def get_palette():
    """Return the current palette (colors may be zero if unsupported)."""
    return _PALETTE


def get_sprites():
    """Return the current sprite set (graphics if supported)."""
    return _SPRITES


def safe_addch(stdscr, y, x, ch, attr=None):
    """Best-effort draw for single characters; ignore tiny terminal errors."""
    try:
        if attr is None:
            stdscr.addch(y, x, ch)
        else:
            stdscr.addch(y, x, ch, attr)
    except curses.error:
        pass


def safe_addstr(stdscr, y, x, text, attr=None):
    """Best-effort draw for strings; ignore tiny terminal errors."""
    try:
        if attr is None:
            stdscr.addstr(y, x, text)
        else:
            stdscr.addstr(y, x, text, attr)
    except curses.error:
        pass


def draw_border(stdscr, height, width):
    """Draw a rectangular border around the playable area."""
    palette = get_palette()
    sprites = get_sprites()
    max_y = height - 1
    max_x = width - 1
    safe_addch(stdscr, 0, 0, sprites["ul"], palette["border"])
    safe_addch(stdscr, 0, max_x, sprites["ur"], palette["border"])
    safe_addch(stdscr, max_y, 0, sprites["ll"], palette["border"])
    safe_addch(stdscr, max_y, max_x, sprites["lr"], palette["border"])
    for x in range(1, max_x):
        safe_addch(stdscr, 0, x, sprites["hline"], palette["border"])
        safe_addch(stdscr, max_y, x, sprites["hline"], palette["border"])
    for y in range(1, max_y):
        safe_addch(stdscr, y, 0, sprites["vline"], palette["border"])
        safe_addch(stdscr, y, max_x, sprites["vline"], palette["border"])


def render(stdscr, height, width, snake, food, score):
    """Render the current game state to the screen."""
    palette = get_palette()
    sprites = get_sprites()
    stdscr.erase()
    draw_border(stdscr, height, width)
    safe_addstr(stdscr, 0, 2, f" Score: {score} ", palette["hud"])

    if food is not None:
        fy, fx = food
        safe_addch(stdscr, fy, fx, sprites["food"], palette["food"])

    head = snake[0]
    safe_addch(stdscr, head[0], head[1], sprites["head"], palette["head"])
    for y, x in list(snake)[1:]:
        safe_addch(stdscr, y, x, sprites["body"], palette["body"])

    stdscr.refresh()


def render_center_message(stdscr, height, width, lines):
    """Render a centered multi-line message (game over, win, etc.)."""
    palette = get_palette()
    start_y = height // 2
    for offset, line in enumerate(lines):
        start_x = max(1, width // 2 - len(line) // 2)
        safe_addstr(
            stdscr, start_y + offset, start_x, line, palette["message"]
        )
    stdscr.refresh()
