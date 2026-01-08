"""Core game rules shared across terminal and Android front ends."""

from dataclasses import dataclass

from .state import make_initial_snake, place_food


@dataclass
class GameState:
    height: int
    width: int
    snake: object
    snake_set: set
    direction: tuple
    food: object
    score: int
    min_y: int
    max_y: int
    min_x: int
    max_x: int

    def set_direction(self, proposed):
        """Update direction, preventing a 180-degree reversal."""
        if proposed is None:
            return False
        if proposed[0] == -self.direction[0] and proposed[1] == -self.direction[1]:
            return False
        if proposed == self.direction:
            return False
        self.direction = proposed
        return True

    def step(self):
        """Advance the game by one tick; return a status string."""
        head_y, head_x = self.snake[0]
        next_head = (head_y + self.direction[0], head_x + self.direction[1])

        if (
            next_head[0] < self.min_y
            or next_head[0] > self.max_y
            or next_head[1] < self.min_x
            or next_head[1] > self.max_x
            or next_head in self.snake_set
        ):
            return "game_over"

        self.snake.appendleft(next_head)
        self.snake_set.add(next_head)

        if next_head == self.food:
            self.score += 1
            self.food = place_food(
                self.height,
                self.width,
                self.snake,
                min_y=self.min_y,
                max_y=self.max_y,
                min_x=self.min_x,
                max_x=self.max_x,
            )
            if self.food is None:
                return "win"
            return "ate"

        tail = self.snake.pop()
        self.snake_set.discard(tail)
        return "moved"


def new_game(height, width, bounds=None):
    """Create a new game state for the given board size."""
    if bounds is None:
        bounds = (1, height - 2, 1, width - 2)
    min_y, max_y, min_x, max_x = bounds
    snake, snake_set = make_initial_snake(height, width)
    food = place_food(
        height, width, snake, min_y=min_y, max_y=max_y, min_x=min_x, max_x=max_x
    )
    return GameState(
        height=height,
        width=width,
        snake=snake,
        snake_set=snake_set,
        direction=(0, 1),
        food=food,
        score=0,
        min_y=min_y,
        max_y=max_y,
        min_x=min_x,
        max_x=max_x,
    )


def compute_speed(length, base_speed=0.12, min_speed=0.05):
    """Return movement speed based on snake length."""
    return max(min_speed, base_speed - (length * 0.002))
