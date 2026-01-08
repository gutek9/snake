"""High score persistence and rendering."""

import curses
import json
import os

from .background import init_starfield, render_starfield, update_starfield
from .rendering import draw_border, draw_centered_text, get_palette

_DEFAULT_PATH = os.path.join(
    os.path.expanduser("~"), ".terminal_snake_scores.json"
)
_MAX_SCORES = 10
_NAME_LEN = 3


def load_scores(path=_DEFAULT_PATH):
    """Load scores from disk; return an empty list on failure."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        scores = []
        for item in data:
            if isinstance(item, dict):
                name = str(item.get("name", "???"))[:_NAME_LEN]
                score = int(item.get("score", 0))
                scores.append({"name": name, "score": score})
            else:
                scores.append({"name": "???", "score": int(item)})
        return sorted(scores, key=lambda row: row["score"], reverse=True)[
            :_MAX_SCORES
        ]
    except (OSError, ValueError, TypeError):
        return []


def save_scores(scores, path=_DEFAULT_PATH):
    """Persist scores to disk, best-effort."""
    try:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(scores, handle)
    except OSError:
        return False
    return True


def record_score(score, name, scores):
    """Insert a new score into the list and keep the top 10."""
    updated = list(scores)
    if score is not None:
        updated.append({"name": name or "???", "score": int(score)})
    updated = sorted(updated, key=lambda row: row["score"], reverse=True)[
        :_MAX_SCORES
    ]
    return updated


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
        display = "".join(initials).ljust(_NAME_LEN, "_")
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
                return "".join(initials).ljust(_NAME_LEN, "_")
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if initials:
                initials.pop()
        elif 32 <= key <= 126 and len(initials) < _NAME_LEN:
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
