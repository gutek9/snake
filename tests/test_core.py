from snake.core import new_game


def test_new_game_bounds_respected():
    state = new_game(20, 20, bounds=(2, 10, 3, 12))
    head_y, head_x = state.snake[0]
    assert 2 <= head_y <= 10
    assert 3 <= head_x <= 12
    if state.food is not None:
        fy, fx = state.food
        assert 2 <= fy <= 10
        assert 3 <= fx <= 12


def test_step_eat_increments_score_and_grows():
    state = new_game(10, 10, bounds=(1, 8, 1, 8))
    head_y, head_x = state.snake[0]
    state.direction = (0, 1)
    state.food = (head_y, head_x + 1)
    before_len = len(state.snake)
    status = state.step()
    assert status == "ate"
    assert state.score == 1
    assert len(state.snake) == before_len + 1


def test_step_game_over_on_wall_collision():
    state = new_game(8, 8, bounds=(1, 6, 1, 6))
    state.snake.clear()
    state.snake.appendleft((1, 1))
    state.snake_set = {(1, 1)}
    state.direction = (-1, 0)
    assert state.step() == "game_over"


def test_step_win_when_no_space():
    state = new_game(4, 4, bounds=(1, 2, 1, 2))
    state.snake.clear()
    state.snake.extend([(1, 1), (1, 2), (2, 2), (2, 1)])
    state.snake_set = set(state.snake)
    state.direction = (0, 1)
    state.food = (1, 2)
    assert state.step() == "win"
