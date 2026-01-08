"""Terminal sizing helpers and related utilities."""

from .rendering import safe_addstr


def ensure_min_size(stdscr, height, width, min_height=10, min_width=20):
    """Validate terminal size and show a helpful message when too small."""
    if height < min_height or width < min_width:
        stdscr.clear()
        message = (
            "Terminal too small. Resize to at least "
            f"{min_width}x{min_height} and try again."
        )
        safe_addstr(stdscr, 0, 0, message[: max(0, width - 1)])
        stdscr.refresh()
        stdscr.getch()
        return False
    return True
