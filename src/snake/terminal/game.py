"""Core game loop for the terminal Snake game."""

import curses
import sys
import time

from .background import init_starfield, update_starfield
from .input import next_direction
from .menu import menu_loop
from .rendering import init_style, render, render_center_message
from .scores import prompt_initials, render_scores
from .terminal import ensure_min_size
from ..core import compute_speed, new_game
from ..scores_store import load_scores, record_score, save_scores


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

    state = new_game(height, width)
    starfield = init_starfield(height, width)

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
                return state.score
            starfield = init_starfield(height, width)
            render(
                stdscr,
                height,
                width,
                state.snake,
                state.food,
                state.score,
                starfield,
            )
            continue
        state.set_direction(next_direction(key, state.direction))

        # Timing phase: keep movement speed stable as the snake grows.
        now = time.monotonic()
        speed = compute_speed(len(state.snake), base_speed=base_speed)
        if now - last_move < speed:
            time.sleep(0.005)
            continue
        last_move = now

        # Collision phase: walls or self.
        status = state.step()
        if status == "game_over":
            break
        if status == "win":
            render(stdscr, height, width, state.snake, state.food, state.score)
            stdscr.nodelay(False)
            render_center_message(
                stdscr,
                height,
                width,
                ["You Win!", f"Final score: {state.score}", "Press any key"],
            )
            stdscr.getch()
            return state.score

        update_starfield(starfield, height, width)
        render(
            stdscr,
            height,
            width,
            state.snake,
            state.food,
            state.score,
            starfield,
        )

    stdscr.nodelay(False)
    render_center_message(
        stdscr,
        height,
        width,
        ["Game Over", f"Final score: {state.score}", "Press any key"],
    )
    stdscr.getch()
    return state.score


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

        starfield = init_starfield(height, width)
        choice = menu_loop(stdscr, height, width, starfield)
        if choice == "Exit":
            return
        if choice == "High Scores":
            render_scores(stdscr, height, width, scores, starfield)
            continue

        stdscr.clear()
        score = _game_loop(stdscr)
        height, width = stdscr.getmaxyx()
        name = prompt_initials(stdscr, height, width)
        scores = record_score(score, name, scores)
        save_scores(scores)


def run():
    """Entry point for the CLI and module execution."""
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("Snake needs an interactive terminal (TTY). Run it in a terminal.")
        return
    curses.wrapper(_main_loop)


if __name__ == "__main__":
    run()
