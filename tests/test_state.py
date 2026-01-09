from snake import state


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


def test_make_initial_snake_respects_bounds():
    snake, snake_set = state.make_initial_snake(20, 20, bounds=(5, 10, 6, 12))
    head_y, head_x = snake[0]
    assert 5 <= head_y <= 10
    assert 6 <= head_x <= 12
    assert head_x - 2 >= 6
    assert snake_set == set(snake)
