"""Game board rendering for the Android front end."""

from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from ..core import new_game
from .theme import NEON


class SnakeBoard(Widget):
    state = ObjectProperty(None)

    def __init__(self, grid_height=20, grid_width=20, **kwargs):
        super().__init__(**kwargs)
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.padding = 12
        self.target_cell = 28
        self.reset()
        Window.bind(on_resize=self._on_resize)

    def reset(self):
        bounds = (0, self.grid_height - 1, 0, self.grid_width - 1)
        self.state = new_game(self.grid_height, self.grid_width, bounds=bounds)
        self._redraw()

    def set_direction(self, direction):
        self.state.set_direction(direction)

    def _on_resize(self, *args):
        self._update_grid()
        self._redraw()

    def _update_grid(self):
        """Resize the logical grid to fit the available pixels."""
        usable_w = max(1, self.width - self.padding * 2)
        usable_h = max(1, self.height - self.padding * 2)
        cols = max(12, int(usable_w / self.target_cell))
        rows = max(12, int(usable_h / self.target_cell))
        if rows != self.grid_height or cols != self.grid_width:
            self.grid_height = rows
            self.grid_width = cols
            self.reset()

    def _grid_bounds(self):
        width = max(1, self.width - self.padding * 2)
        height = max(1, self.height - self.padding * 2)
        cell = min(width / self.grid_width, height / self.grid_height)
        origin_x = self.x + (self.width - cell * self.grid_width) / 2
        origin_y = self.y + (self.height - cell * self.grid_height) / 2
        return origin_x, origin_y, cell

    def grid_bounds(self):
        """Return the grid bounds in pixels for layout calculations."""
        origin_x, origin_y, cell = self._grid_bounds()
        grid_w = cell * self.grid_width
        grid_h = cell * self.grid_height
        return origin_x, origin_y, grid_w, grid_h, cell

    def _cell_rect(self, y, x):
        origin_x, origin_y, cell = self._grid_bounds()
        return (
            origin_x + x * cell,
            origin_y + (self.grid_height - 1 - y) * cell,
            cell,
            cell,
        )

    def _redraw(self):
        self.canvas.clear()
        with self.canvas:
            Color(*NEON["bg"])
            Rectangle(pos=self.pos, size=self.size)

            origin_x, origin_y, cell = self._grid_bounds()
            grid_w = cell * self.grid_width
            grid_h = cell * self.grid_height
            Color(*NEON["cyan"])
            Line(rectangle=(origin_x, origin_y, grid_w, grid_h), width=2.2)
            Color(0.2, 0.7, 1.0, 0.2)
            Line(
                rectangle=(origin_x + 3, origin_y + 3, grid_w - 6, grid_h - 6),
                width=1.4,
            )

            # Subtle scanlines for a retro neon effect.
            Color(0.08, 0.4, 0.55, 0.18)
            line_y = origin_y + 4
            while line_y < origin_y + grid_h - 4:
                Line(
                    points=[origin_x + 2, line_y, origin_x + grid_w - 2, line_y],
                    width=1,
                )
                line_y += 8

            if self.state.food is not None:
                fy, fx = self.state.food
                x, y, w, h = self._cell_rect(fy, fx)
                Color(*NEON["yellow"])
                RoundedRectangle(
                    pos=(x + 1, y + 1), size=(w - 2, h - 2), radius=[6]
                )

            for idx, (y, x) in enumerate(self.state.snake):
                px, py, w, h = self._cell_rect(y, x)
                if idx == 0:
                    # Glow trail under the head.
                    Color(0.3, 1.0, 0.7, 0.45)
                    RoundedRectangle(
                        pos=(px - 3, py - 3), size=(w + 6, h + 6), radius=[8]
                    )
                    Color(*NEON["green"])
                else:
                    Color(0.15, 0.7, 1.0, 1.0)
                RoundedRectangle(
                    pos=(px + 1, py + 1), size=(w - 2, h - 2), radius=[6]
                )
