"""High score persistence and rendering."""

import json
import os

from .rendering import draw_border, draw_centered_text, get_palette

_DEFAULT_PATH = os.path.join(
    os.path.expanduser("~"), ".terminal_snake_scores.json"
)


def load_scores(path=_DEFAULT_PATH):
    """Load scores from disk; return an empty list on failure."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        scores = [int(value) for value in data]
        return sorted(scores, reverse=True)[:10]
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


def record_score(score, scores):
    """Insert a new score into the list and keep the top 10."""
    updated = list(scores)
    if score is not None:
        updated.append(int(score))
    updated = sorted(updated, reverse=True)[:10]
    return updated


def render_scores(stdscr, height, width, scores):
    """Render the high-score list and wait for a keypress."""
    palette = get_palette()
    stdscr.erase()
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
            line = f"{idx:>2}. {score}"
            draw_centered_text(
                stdscr, start_y + idx - 1, width, line, palette["hud"]
            )

    footer = "Press any key to return"
    draw_centered_text(stdscr, height - 2, width, footer, palette["hud"])
    stdscr.refresh()
    stdscr.getch()
