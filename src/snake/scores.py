"""High score persistence and rendering."""

import json
import os

from .rendering import draw_border, get_palette, safe_addstr

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
    safe_addstr(
        stdscr,
        2,
        max(1, width // 2 - len(title) // 2),
        title,
        palette["hud"],
    )

    if not scores:
        safe_addstr(
            stdscr,
            height // 2,
            max(1, width // 2 - len("No scores yet") // 2),
            "No scores yet",
            palette["message"],
        )
    else:
        start_y = height // 2 - len(scores) // 2
        for idx, score in enumerate(scores, start=1):
            line = f"{idx:>2}. {score}"
            safe_addstr(
                stdscr,
                start_y + idx - 1,
                max(1, width // 2 - len(line) // 2),
                line,
                palette["hud"],
            )

    footer = "Press any key to return"
    safe_addstr(
        stdscr,
        height - 2,
        max(1, width // 2 - len(footer) // 2),
        footer,
        palette["hud"],
    )
    stdscr.refresh()
    stdscr.getch()
