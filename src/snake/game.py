import curses
import random
import sys
import time
from collections import deque


def _place_food(height, width, snake):
    max_cells = (height - 2) * (width - 2)
    if len(snake) >= max_cells:
        return None
    while True:
        y = random.randint(1, height - 2)
        x = random.randint(1, width - 2)
        if (y, x) not in snake:
            return (y, x)


def _safe_addch(stdscr, y, x, ch):
    try:
        stdscr.addch(y, x, ch)
    except curses.error:
        pass


def _safe_addstr(stdscr, y, x, text):
    try:
        stdscr.addstr(y, x, text)
    except curses.error:
        pass


def _draw_border(stdscr, height, width):
    max_y = height - 1
    max_x = width - 1
    for x in range(width):
        _safe_addch(stdscr, 0, x, "#")
        _safe_addch(stdscr, max_y, x, "#")
    for y in range(height):
        _safe_addch(stdscr, y, 0, "#")
        _safe_addch(stdscr, y, max_x, "#")


def _render(stdscr, height, width, snake, food, score):
    stdscr.erase()
    _draw_border(stdscr, height, width)
    _safe_addstr(stdscr, 0, 2, f" Score: {score} ")

    if food is not None:
        fy, fx = food
        _safe_addch(stdscr, fy, fx, "*")

    head = snake[0]
    _safe_addch(stdscr, head[0], head[1], "@")
    for y, x in list(snake)[1:]:
        _safe_addch(stdscr, y, x, "o")

    stdscr.refresh()


def _next_direction(key, current):
    mapping = {
        ord("w"): (-1, 0),
        ord("s"): (1, 0),
        ord("a"): (0, -1),
        ord("d"): (0, 1),
        curses.KEY_UP: (-1, 0),
        curses.KEY_DOWN: (1, 0),
        curses.KEY_LEFT: (0, -1),
        curses.KEY_RIGHT: (0, 1),
    }
    if key not in mapping:
        return current
    proposed = mapping[key]
    # Prevent reversing into itself.
    if (proposed[0] == -current[0] and proposed[1] == -current[1]):
        return current
    return proposed


def _ensure_min_size(stdscr, height, width):
    min_height = 10
    min_width = 20
    if height < min_height or width < min_width:
        stdscr.clear()
        message = (
            "Terminal too small. Resize to at least "
            f"{min_width}x{min_height} and try again."
        )
        _safe_addstr(stdscr, 0, 0, message[: max(0, width - 1)])
        stdscr.refresh()
        stdscr.getch()
        return False
    return True


def _game_loop(stdscr):
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)

    height, width = stdscr.getmaxyx()
    if not _ensure_min_size(stdscr, height, width):
        return 0

    start_y = height // 2
    start_x = width // 2
    snake = deque(
        [
            (start_y, start_x),
            (start_y, start_x - 1),
            (start_y, start_x - 2),
        ]
    )
    snake_set = {pos for pos in snake}
    direction = (0, 1)
    food = _place_food(height, width, snake)
    score = 0

    last_move = time.monotonic()
    base_speed = 0.12

    while True:
        key = stdscr.getch()
        if key in (ord("q"), ord("Q")):
            break
        if key == curses.KEY_RESIZE:
            height, width = stdscr.getmaxyx()
            if not _ensure_min_size(stdscr, height, width):
                return score
            _render(stdscr, height, width, snake, food, score)
            continue
        direction = _next_direction(key, direction)

        now = time.monotonic()
        speed = max(0.05, base_speed - (len(snake) * 0.002))
        if now - last_move < speed:
            time.sleep(0.005)
            continue
        last_move = now

        head_y, head_x = snake[0]
        next_head = (head_y + direction[0], head_x + direction[1])

        if (
            next_head[0] <= 0
            or next_head[0] >= height - 1
            or next_head[1] <= 0
            or next_head[1] >= width - 1
            or next_head in snake_set
        ):
            break

        snake.appendleft(next_head)
        snake_set.add(next_head)

        if next_head == food:
            score += 1
            food = _place_food(height, width, snake)
            if food is None:
                _render(stdscr, height, width, snake, food, score)
                stdscr.nodelay(False)
                _safe_addstr(
                    stdscr,
                    height // 2,
                    max(1, width // 2 - 4),
                    "You Win!",
                )
                _safe_addstr(
                    stdscr,
                    height // 2 + 1,
                    max(1, width // 2 - 12),
                    f"Final score: {score}",
                )
                _safe_addstr(
                    stdscr,
                    height // 2 + 2,
                    max(1, width // 2 - 12),
                    "Press any key",
                )
                stdscr.refresh()
                stdscr.getch()
                return score
        else:
            tail = snake.pop()
            snake_set.discard(tail)

        _render(stdscr, height, width, snake, food, score)

    stdscr.nodelay(False)
    _safe_addstr(stdscr, height // 2, max(1, width // 2 - 6), "Game Over")
    _safe_addstr(
        stdscr,
        height // 2 + 1,
        max(1, width // 2 - 12),
        f"Final score: {score}",
    )
    _safe_addstr(
        stdscr, height // 2 + 2, max(1, width // 2 - 12), "Press any key"
    )
    stdscr.refresh()
    stdscr.getch()
    return score


def run():
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("Snake needs an interactive terminal (TTY). Run it in a terminal.")
        return
    curses.wrapper(_game_loop)


if __name__ == "__main__":
    run()
