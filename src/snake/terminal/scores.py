"""Terminal high score UI and initials prompt."""

import curses

from .background import init_starfield, render_starfield, update_starfield
from .rendering import draw_border, draw_centered_text, get_palette
from ..scores_store import NAME_LEN


def prompt_initials(stdscr, height, width):
    """Prompt the player for arcade-style initials (3 characters)."""
    palette = get_palette()
    initials = []

    stdscr.nodelay(False)
    while True:
        stdscr.erase()
        draw_border(stdscr, height, width)
        draw_centered_text(
            stdscr, 2, width, "New High Score!", palette["hud"]
        )
        draw_centered_text(
            stdscr,
            height // 2 - 1,
            width,
            "Enter your initials",
            palette["hud"],
        )
        display = "".join(initials).ljust(NAME_LEN, "_")
        draw_centered_text(
            stdscr, height // 2 + 1, width, display, palette["message"]
        )
        draw_centered_text(
            stdscr, height - 2, width, "Enter to confirm", palette["hud"]
        )
        stdscr.refresh()

        key = stdscr.getch()
        if key in (10, 13, curses.KEY_ENTER):
            if initials:
                return "".join(initials).ljust(NAME_LEN, "_")
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if initials:
                initials.pop()
        elif 32 <= key <= 126 and len(initials) < NAME_LEN:
            initials.append(chr(key).upper())


def render_scores(stdscr, height, width, scores, starfield):
    """Render the high-score list and wait for a keypress."""
    palette = get_palette()
    stdscr.timeout(80)

    while True:
        update_starfield(starfield, height, width)
        stdscr.erase()
        render_starfield(stdscr, height, width, starfield)
        draw_border(stdscr, height, width)

        title = "High Scores"
        draw_centered_text(stdscr, 2, width, title, palette["hud"])

        if not scores:
            draw_centered_text(
                stdscr, height // 2, width, "No scores yet", palette["message"]
            )
        else:
            start_y = height // 2 - len(scores) // 2
            for idx, score in enumerate(scores, start=1):
                line = f"{idx:>2}. {score['name']:<3}  {score['score']}"
                draw_centered_text(
                    stdscr, start_y + idx - 1, width, line, palette["hud"]
                )

        draw_centered_text(
            stdscr,
            height - 2,
            width,
            "Press any key to return",
            palette["hud"],
        )
        stdscr.refresh()

        key = stdscr.getch()
        if key == -1:
            continue
        if key == curses.KEY_RESIZE:
            height, width = stdscr.getmaxyx()
            starfield.update(init_starfield(height, width))
            continue
        return
