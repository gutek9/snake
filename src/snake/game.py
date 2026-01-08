"""Core game loop for the terminal Snake game."""

import curses
import sys
import time

from .input import next_direction
from .menu import menu_loop
from .rendering import init_style, render, render_center_message
from .scores import load_scores, record_score, render_scores, save_scores
from .state import make_initial_snake, place_food
from .terminal import ensure_min_size


def _game_loop(stdscr):
    """Run the main game loop; called by curses.wrapper."""
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)

    # Bootstrap the initial board and starting state.
    height, width = stdscr.getmaxyx()
    if not ensure_min_size(stdscr, height, width):
        return 0

    snake, snake_set = make_initial_snake(height, width)
    direction = (0, 1)
    food = place_food(height, width, snake)
    score = 0

    last_move = time.monotonic()
    base_speed = 0.12

    while True:
        # Input phase: handle quit, resize, and direction changes.
        key = stdscr.getch()
        if key in (ord("q"), ord("Q")):
            break
        if key == curses.KEY_RESIZE:
            height, width = stdscr.getmaxyx()
            if not ensure_min_size(stdscr, height, width):
                return score
            render(stdscr, height, width, snake, food, score)
            continue
        direction = next_direction(key, direction)

        # Timing phase: keep movement speed stable as the snake grows.
        now = time.monotonic()
        speed = max(0.05, base_speed - (len(snake) * 0.002))
        if now - last_move < speed:
            time.sleep(0.005)
            continue
        last_move = now

        # Movement phase: compute the next head position.
        head_y, head_x = snake[0]
        next_head = (head_y + direction[0], head_x + direction[1])

        # Collision phase: walls or self.
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

        # State update: grow on food, otherwise move tail forward.
        if next_head == food:
            score += 1
            food = place_food(height, width, snake)
            if food is None:
                render(stdscr, height, width, snake, food, score)
                stdscr.nodelay(False)
                render_center_message(
                    stdscr,
                    height,
                    width,
                    ["You Win!", f"Final score: {score}", "Press any key"],
                )
                stdscr.getch()
                return score
        else:
            tail = snake.pop()
            snake_set.discard(tail)

        render(stdscr, height, width, snake, food, score)

    stdscr.nodelay(False)
    render_center_message(
        stdscr,
        height,
        width,
        ["Game Over", f"Final score: {score}", "Press any key"],
    )
    stdscr.getch()
    return score


def _main_loop(stdscr):
    """Menu-driven entry point for the game session."""
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    init_style(stdscr)

    scores = load_scores()

    while True:
        height, width = stdscr.getmaxyx()
        if not ensure_min_size(stdscr, height, width):
            return

        choice = menu_loop(stdscr, height, width)
        if choice == "Exit":
            return
        if choice == "High Scores":
            render_scores(stdscr, height, width, scores)
            continue

        stdscr.clear()
        score = _game_loop(stdscr)
        scores = record_score(score, scores)
        save_scores(scores)


def run():
    """Entry point for the CLI and module execution."""
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("Snake needs an interactive terminal (TTY). Run it in a terminal.")
        return
    curses.wrapper(_main_loop)


if __name__ == "__main__":
    run()
