import curses

from snake import state
from snake.terminal import input as input_mod
from snake.terminal import rendering, terminal


class DummyStdScr:
    def __init__(self):
        self.calls = []
        self.getch_called = False
        self.erased = False
        self.refreshed = False
        self.cleared = False

    def addch(self, y, x, ch):
        self.calls.append(("addch", y, x, ch))

    def addstr(self, y, x, text):
        self.calls.append(("addstr", y, x, text))

    def erase(self):
        self.erased = True

    def refresh(self):
        self.refreshed = True

    def clear(self):
        self.cleared = True

    def getch(self):
        self.getch_called = True
        return 0


def test_place_food_skips_snake(monkeypatch):
    seq = iter([1, 1, 2, 3])

    def fake_randint(low, high):
        return next(seq)

    monkeypatch.setattr(state.random, "randint", fake_randint)
    snake = [(1, 1), (1, 2)]

    food = state.place_food(10, 10, snake)

    assert food == (2, 3)


def test_place_food_returns_none_when_full():
    snake = [(1, 1)]

    food = state.place_food(3, 3, snake)

    assert food is None


def test_next_direction_ignores_unknown_key():
    assert input_mod.next_direction(ord("x"), (0, 1)) == (0, 1)


def test_next_direction_prevents_reverse():
    assert input_mod.next_direction(ord("a"), (0, 1)) == (0, 1)


def test_next_direction_allows_change():
    assert input_mod.next_direction(curses.KEY_UP, (0, 1)) == (-1, 0)


def test_safe_addch_ignores_curses_error():
    class Boom:
        def addch(self, y, x, ch):
            raise curses.error("nope")

    rendering.safe_addch(Boom(), 1, 1, "#")


def test_safe_addstr_ignores_curses_error():
    class Boom:
        def addstr(self, y, x, text):
            raise curses.error("nope")

    rendering.safe_addstr(Boom(), 1, 1, "hi")


def test_draw_border_marks_edges(monkeypatch):
    calls = []

    def fake_addch(stdscr, y, x, ch, *args, **kwargs):
        calls.append((y, x, ch))

    monkeypatch.setattr(rendering, "safe_addch", fake_addch)

    rendering.draw_border(object(), 4, 6)

    sprites = rendering.get_sprites()
    expected = {
        (0, 0, sprites["ul"]),
        (0, 5, sprites["ur"]),
        (3, 0, sprites["ll"]),
        (3, 5, sprites["lr"]),
        (0, 2, sprites["hline"]),
        (2, 0, sprites["vline"]),
    }
    assert expected.issubset(set(calls))


def test_render_draws_snake_food_and_score(monkeypatch):
    stdscr = DummyStdScr()
    addch_calls = []
    addstr_calls = []
    border_calls = []

    def fake_addch(stdscr_arg, y, x, ch, *args, **kwargs):
        addch_calls.append((y, x, ch))

    def fake_addstr(stdscr_arg, y, x, text, *args, **kwargs):
        addstr_calls.append((y, x, text))

    def fake_border(stdscr_arg, height, width):
        border_calls.append((height, width))

    monkeypatch.setattr(rendering, "safe_addch", fake_addch)
    monkeypatch.setattr(rendering, "safe_addstr", fake_addstr)
    monkeypatch.setattr(rendering, "draw_border", fake_border)

    snake = [(5, 5), (5, 4), (5, 3)]
    food = (3, 3)

    rendering.render(stdscr, 10, 20, snake, food, 3)

    sprites = rendering.get_sprites()
    assert stdscr.erased is True
    assert stdscr.refreshed is True
    assert border_calls == [(10, 20)]
    assert (3, 3, sprites["food"]) in addch_calls
    assert (5, 5, sprites["head"]) in addch_calls
    assert (5, 4, sprites["body"]) in addch_calls
    assert any("Score: 3" in text for _, _, text in addstr_calls)


def test_ensure_min_size_rejects_small_terminal():
    stdscr = DummyStdScr()

    ok = terminal.ensure_min_size(stdscr, 5, 10)

    assert ok is False
    assert stdscr.cleared is True
    assert stdscr.refreshed is True
    assert stdscr.getch_called is True
    assert any("Terminal too small" in call[3] for call in stdscr.calls)


def test_ensure_min_size_accepts_large_terminal():
    stdscr = DummyStdScr()

    ok = terminal.ensure_min_size(stdscr, 20, 40)

    assert ok is True
    assert stdscr.getch_called is False
