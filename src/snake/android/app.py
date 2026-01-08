"""Kivy front end for Android-compatible Snake."""

import os
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from ..core import compute_speed, new_game
from ..scores_store import NAME_LEN, load_scores, record_score, save_scores


_DIRECTIONS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}

_NEON = {
    "bg": (0.03, 0.04, 0.08, 1.0),
    "panel": (0.06, 0.08, 0.14, 1.0),
    "cyan": (0.2, 0.9, 1.0, 1.0),
    "magenta": (1.0, 0.3, 0.8, 1.0),
    "yellow": (1.0, 0.95, 0.4, 1.0),
    "green": (0.35, 1.0, 0.6, 1.0),
    "white": (0.98, 0.99, 1.0, 1.0),
}


class NeonButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = _NEON["white"]
        self.font_size = 20
        self.bold = True
        self._pulse = 0.0
        self._pulse_dir = 1
        self.bind(pos=self._redraw, size=self._redraw)

    def tick(self, dt):
        self._pulse += dt * self._pulse_dir
        if self._pulse >= 1.0:
            self._pulse = 1.0
            self._pulse_dir = -1
        elif self._pulse <= 0.0:
            self._pulse = 0.0
            self._pulse_dir = 1
        self._redraw()

    def _redraw(self, *_args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*_NEON["panel"])
            RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
            glow = 0.6 + (self._pulse * 0.4)
            Color(_NEON["cyan"][0], _NEON["cyan"][1], _NEON["cyan"][2], glow)
            Line(rounded_rectangle=(
                self.x + 2,
                self.y + 2,
                self.width - 4,
                self.height - 4,
                12,
            ), width=1.2)


class NeonPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *_args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*_NEON["panel"])
            RoundedRectangle(pos=self.pos, size=self.size, radius=[16])
            Color(*_NEON["magenta"])
            Line(rounded_rectangle=(
                self.x + 1,
                self.y + 1,
                self.width - 2,
                self.height - 2,
                16,
            ), width=1.0)


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
            Color(*_NEON["bg"])
            Rectangle(pos=self.pos, size=self.size)

            origin_x, origin_y, cell = self._grid_bounds()
            grid_w = cell * self.grid_width
            grid_h = cell * self.grid_height
            Color(*_NEON["cyan"])
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
                Color(*_NEON["yellow"])
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
                    Color(*_NEON["green"])
                else:
                    Color(0.15, 0.7, 1.0, 1.0)
                RoundedRectangle(
                    pos=(px + 1, py + 1), size=(w - 2, h - 2), radius=[6]
                )


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = NeonPanel(orientation="vertical", padding=28, spacing=18)
        title = Label(
            text="[b]CODEX SNAKE[/b]",
            font_size=52,
            size_hint=(1, 0.3),
            color=_NEON["magenta"],
            markup=True,
        )
        subtitle = Label(
            text="ARCADE SYSTEM READY",
            font_size=16,
            size_hint=(1, 0.08),
            color=_NEON["cyan"],
        )
        layout.add_widget(title)
        layout.add_widget(subtitle)

        btn_new = NeonButton(text="NEW GAME", size_hint=(1, 0.22))
        btn_scores = NeonButton(text="HIGH SCORES", size_hint=(1, 0.22))
        btn_exit = NeonButton(text="EXIT", size_hint=(1, 0.22))
        self._pulse_buttons = [btn_new, btn_scores, btn_exit]

        btn_new.bind(on_press=lambda *_: setattr(self.manager, "current", "game"))
        btn_scores.bind(
            on_press=lambda *_: setattr(self.manager, "current", "scores")
        )
        btn_exit.bind(on_press=lambda *_: App.get_running_app().stop())

        layout.add_widget(btn_new)
        layout.add_widget(btn_scores)
        layout.add_widget(btn_exit)
        self.add_widget(layout)


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_move = time.monotonic()
        self.base_speed = 0.12
        self._tick_event = None
        self._scores_path = None

        root = BoxLayout(orientation="vertical", spacing=8, padding=10)
        self.score_label = Label(
            text="Score: 0",
            size_hint=(1, 0.1),
            color=_NEON["white"],
            font_size=26,
        )
        root.add_widget(self.score_label)

        self.board = SnakeBoard()
        root.add_widget(self.board)

        controls = NeonPanel(size_hint=(1, 0.26), padding=8)
        dpad = GridLayout(cols=3, rows=3, spacing=6)
        btn_up = NeonButton(text="▲")
        btn_left = NeonButton(text="◀")
        btn_down = NeonButton(text="▼")
        btn_right = NeonButton(text="▶")
        self._pulse_buttons = [btn_left, btn_up, btn_down, btn_right]
        for btn, direction in (
            (btn_left, "left"),
            (btn_up, "up"),
            (btn_down, "down"),
            (btn_right, "right"),
        ):
            btn.bind(on_press=lambda _btn, d=direction: self._set_dir(d))
        dpad.add_widget(Widget())
        dpad.add_widget(btn_up)
        dpad.add_widget(Widget())
        dpad.add_widget(btn_left)
        dpad.add_widget(Widget())
        dpad.add_widget(btn_right)
        dpad.add_widget(Widget())
        dpad.add_widget(btn_down)
        dpad.add_widget(Widget())
        controls.add_widget(dpad)
        root.add_widget(controls)
        self.add_widget(root)

    def on_pre_enter(self, *args):
        self.board.reset()
        self.last_move = time.monotonic()
        self.score_label.text = "Score: 0"
        if self._tick_event is None:
            self._tick_event = Clock.schedule_interval(self._tick, 1 / 30)

    def on_leave(self, *args):
        if self._tick_event is not None:
            self._tick_event.cancel()
            self._tick_event = None

    def set_scores_path(self, path):
        self._scores_path = path

    def _set_dir(self, key):
        self.board.set_direction(_DIRECTIONS[key])

    def _tick(self, _dt):
        now = time.monotonic()
        speed = compute_speed(len(self.board.state.snake), self.base_speed)
        if now - self.last_move < speed:
            return
        self.last_move = now

        status = self.board.state.step()
        self.score_label.text = f"Score: {self.board.state.score}"
        self.board._redraw()

        if status in ("game_over", "win"):
            self._show_game_over(status)

    def _show_game_over(self, status):
        title = "You Win!" if status == "win" else "Game Over"
        if self._tick_event is not None:
            self._tick_event.cancel()
            self._tick_event = None
        prompt = NeonPanel(orientation="vertical", spacing=8, padding=12)
        prompt.add_widget(Label(text=title, color=_NEON["white"], font_size=24))
        prompt.add_widget(Label(text="Enter your initials", color=_NEON["white"]))

        text = TextInput(
            text="",
            multiline=False,
            halign="center",
            font_size=24,
            foreground_color=_NEON["white"],
            background_color=_NEON["panel"],
        )
        prompt.add_widget(text)

        ok_btn = NeonButton(text="Save", size_hint=(1, 0.4))
        prompt.add_widget(ok_btn)

        popup = Popup(title=title, content=prompt, size_hint=(0.8, 0.6))

        def on_save(*_args):
            initials = (text.text.strip().upper() or "???")[:NAME_LEN]
            scores = load_scores(self._scores_path)
            scores = record_score(self.board.state.score, initials, scores)
            save_scores(scores, self._scores_path)
            popup.dismiss()
            self.manager.current = "menu"

        ok_btn.bind(on_press=on_save)
        popup.open()


class ScoresScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._scores_path = None
        self._label = Label(
            text="", halign="center", valign="middle", color=_NEON["white"]
        )

        layout = NeonPanel(orientation="vertical", padding=16, spacing=8)
        layout.add_widget(Label(text="High Scores", font_size=28, color=_NEON["white"]))
        layout.add_widget(self._label)
        back = NeonButton(text="Back", size_hint=(1, 0.2))
        self._pulse_buttons = [back]
        back.bind(on_press=lambda *_: setattr(self.manager, "current", "menu"))
        layout.add_widget(back)
        self.add_widget(layout)

    def set_scores_path(self, path):
        self._scores_path = path

    def on_pre_enter(self, *args):
        self._label.text_size = (self.width, None)
        scores = load_scores(self._scores_path)
        if not scores:
            self._label.text = "No scores yet"
            return
        lines = [
            f"{idx:>2}. {row['name']:<3}  {row['score']}"
            for idx, row in enumerate(scores, start=1)
        ]
        self._label.text = "\n".join(lines)


class SnakeApp(App):
    def build(self):
        Window.clearcolor = _NEON["bg"]
        scores_path = os.path.join(self.user_data_dir, "scores.json")

        sm = ScreenManager()
        menu = MenuScreen(name="menu")
        game = GameScreen(name="game")
        scores = ScoresScreen(name="scores")

        game.set_scores_path(scores_path)
        scores.set_scores_path(scores_path)

        sm.add_widget(menu)
        sm.add_widget(game)
        sm.add_widget(scores)
        self._pulse_targets = [
            *menu._pulse_buttons,
            *game._pulse_buttons,
            *scores._pulse_buttons,
        ]
        Clock.schedule_interval(self._pulse_tick, 1 / 24)
        return sm

    def _pulse_tick(self, dt):
        for btn in self._pulse_targets:
            btn.tick(dt)
