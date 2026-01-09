"""Kivy screens for the Android front end."""

import math
import random
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from ..core import compute_speed
from ..scores_store import NAME_LEN, load_scores, record_score, save_scores
from .board import SnakeBoard
from .overlay import CyberOverlay
from .theme import DIRECTIONS, NEON
from .ui import NeonButton, NeonPanel, SpaceBackdrop, TitleOverlay


def _is_high_score(score, scores_path):
    """Check if the score beats the current best."""
    scores = load_scores(scores_path)
    if not scores:
        return score > 0
    return score >= max(row["score"] for row in scores)


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._audio = None
        self._title = None
        self._flash_phase = 0.0
        self._menu_anim = None
        layout = NeonPanel(orientation="vertical", padding=28, spacing=18)
        title = Label(
            text="[b]CODEX SNAKE[/b]",
            font_size=52,
            size_hint=(1, 0.3),
            color=NEON["magenta"],
            markup=True,
        )
        self._title = title
        subtitle = Label(
            text="ARCADE SYSTEM READY",
            font_size=16,
            size_hint=(1, 0.08),
            color=NEON["cyan"],
        )
        layout.add_widget(title)
        layout.add_widget(subtitle)

        btn_new = NeonButton(text="NEW GAME", size_hint=(1, 0.22))
        btn_scores = NeonButton(text="HIGH SCORES", size_hint=(1, 0.22))
        btn_exit = NeonButton(text="EXIT", size_hint=(1, 0.22))
        self._pulse_buttons = [btn_new, btn_scores, btn_exit]

        btn_new.bind(on_press=lambda *_: setattr(self.manager, "current", "game"))
        btn_scores.bind(on_press=lambda *_: setattr(self.manager, "current", "scores"))
        btn_exit.bind(on_press=lambda *_: App.get_running_app().stop())

        layout.add_widget(btn_new)
        layout.add_widget(btn_scores)
        layout.add_widget(btn_exit)
        self.add_widget(layout)

    def set_audio(self, audio):
        self._audio = audio

    def on_pre_enter(self, *args):
        if self._menu_anim is None:
            self._menu_anim = Clock.schedule_interval(self._tick_menu, 1 / 20)

    def on_leave(self, *args):
        if self._menu_anim is not None:
            self._menu_anim.cancel()
            self._menu_anim = None

    def _tick_menu(self, dt):
        self._flash_phase += dt * 1.8
        if random.random() < 0.08:
            glow = 0.25
        else:
            glow = 0.65 + (math.sin(self._flash_phase) * 0.25)
        self._title.color = (
            NEON["magenta"][0],
            NEON["magenta"][1],
            NEON["magenta"][2],
            max(0.3, min(1.0, glow)),
        )
        pulse = 0.75 + (math.sin(self._flash_phase * 1.3) * 0.2)
        for btn in self._pulse_buttons:
            btn.color = (
                NEON["white"][0],
                NEON["white"][1],
                NEON["white"][2],
                max(0.5, min(1.0, pulse)),
            )


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_move = time.monotonic()
        self.base_speed = 0.12
        self._tick_event = None
        self._scores_path = None
        self._audio = None

        self.backdrop = SpaceBackdrop(size_hint=(1, 1))
        self.add_widget(self.backdrop)

        root = BoxLayout(orientation="vertical", spacing=8, padding=10)
        hud = NeonPanel(size_hint=(1, 0.12), padding=10)
        self._hud_pulse = 0.0
        self._hud_dir = 1
        self._hud_anim = Clock.schedule_interval(self._tick_hud, 1 / 16)
        self.score_label = Label(
            text="[b]SCORE 0000[/b]",
            size_hint=(1, 1),
            color=NEON["magenta"],
            font_size=34,
            markup=True,
        )
        hud.add_widget(self.score_label)
        root.add_widget(hud)

        self.board = SnakeBoard()
        self.board.bind(pos=self._layout_overlays, size=self._layout_overlays)
        root.add_widget(self.board)

        controls = NeonPanel(size_hint=(1, 0.26), padding=8)
        dpad = GridLayout(cols=3, rows=3, spacing=6)
        btn_up = NeonButton(text="UP")
        btn_left = NeonButton(text="LEFT")
        btn_down = NeonButton(text="DOWN")
        btn_right = NeonButton(text="RIGHT")
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

        self.overlay_left = CyberOverlay(align="left", show_matrix=False)
        self.overlay_left.bind_stats(self._hud_stats)
        self.overlay_right = TitleOverlay()
        self.add_widget(self.overlay_left)
        self.add_widget(self.overlay_right)
        Clock.schedule_once(self._layout_overlays, 0)

    def _layout_overlays(self, *_args):
        origin_x, origin_y, grid_w, grid_h, _cell = self.board.grid_bounds()
        left_gutter = origin_x - self.board.x
        right_gutter = (self.board.right) - (origin_x + grid_w)
        margin = 8
        min_width = 64

        left_width = max(0, left_gutter - margin)
        if left_width >= min_width:
            self.overlay_left.opacity = 1.0
            self.overlay_left.size = (left_width, grid_h)
            self.overlay_left.pos = (self.board.x + margin / 2, origin_y)
        else:
            self.overlay_left.opacity = 0.0

        right_width = max(0, right_gutter - margin)
        if right_width >= min_width:
            self.overlay_right.opacity = 1.0
            self.overlay_right.size = (right_width, grid_h)
            self.overlay_right.pos = (origin_x + grid_w + margin / 2, origin_y)
        else:
            self.overlay_right.opacity = 0.0

    def _tick_hud(self, dt):
        self._hud_pulse += dt * self._hud_dir
        if self._hud_pulse >= 1.0:
            self._hud_pulse = 1.0
            self._hud_dir = -1
        elif self._hud_pulse <= 0.0:
            self._hud_pulse = 0.0
            self._hud_dir = 1
        glow = 0.5 + self._hud_pulse * 0.4
        self.score_label.color = (
            NEON["magenta"][0],
            NEON["magenta"][1],
            NEON["magenta"][2],
            glow,
        )

    def on_pre_enter(self, *args):
        self.board.reset()
        self.last_move = time.monotonic()
        self.score_label.text = "[b]SCORE 0000[/b]"
        if self._tick_event is None:
            self._tick_event = Clock.schedule_interval(self._tick, 1 / 30)

    def on_leave(self, *args):
        if self._tick_event is not None:
            self._tick_event.cancel()
            self._tick_event = None

    def set_scores_path(self, path):
        self._scores_path = path

    def set_audio(self, audio):
        self._audio = audio

    def _set_dir(self, key):
        changed = self.board.state.set_direction(DIRECTIONS[key])
        if changed and self._audio is not None:
            self._audio.play_chord("turn", [520, 660], 60, volume=0.5)

    def _tick(self, _dt):
        now = time.monotonic()
        speed = compute_speed(len(self.board.state.snake), self.base_speed)
        if now - self.last_move < speed:
            return
        self.last_move = now

        status = self.board.state.step()
        self.score_label.text = f"[b]SCORE {self.board.state.score:04d}[/b]"
        self.board._redraw()

        if status == "ate" and self._audio is not None:
            self._audio.play_chord("eat", [740, 880, 990], 80, volume=0.6)

        if status in ("game_over", "win"):
            if self._audio is not None and _is_high_score(
                self.board.state.score, self._scores_path
            ):
                self._audio.play_chord(
                    "high_score", [880, 1100, 1320], 140, volume=0.7
                )
            self._show_game_over(status)

    def _hud_stats(self):
        speed = compute_speed(len(self.board.state.snake), self.base_speed)
        speed_pct = max(0, min(99, int((1.0 - speed / 0.2) * 99)))
        length = min(99, len(self.board.state.snake))
        power = max(10, min(99, 30 + length))
        sys = (power + speed_pct) % 99
        dir_map = {(0, 1): "R", (0, -1): "L", (1, 0): "D", (-1, 0): "U"}
        direction = dir_map.get(self.board.state.direction, "?")
        return {
            "sys": sys,
            "spd": speed_pct,
            "len": length,
            "pwr": power,
            "scr": self.board.state.score,
            "dir": direction,
        }

    def _show_game_over(self, status):
        title = "You Win!" if status == "win" else "Game Over"
        if self._tick_event is not None:
            self._tick_event.cancel()
            self._tick_event = None
        prompt = NeonPanel(orientation="vertical", spacing=8, padding=12)
        prompt.add_widget(Label(text=title, color=NEON["white"], font_size=24))
        prompt.add_widget(Label(text="Enter your initials", color=NEON["white"]))

        text = TextInput(
            text="",
            multiline=False,
            halign="center",
            font_size=24,
            foreground_color=NEON["white"],
            background_color=NEON["panel"],
        )
        prompt.add_widget(text)

        actions = BoxLayout(orientation="horizontal", spacing=8, size_hint=(1, 0.4))
        ok_btn = NeonButton(text="Save")
        cancel_btn = NeonButton(text="Cancel")
        actions.add_widget(ok_btn)
        actions.add_widget(cancel_btn)
        prompt.add_widget(actions)

        popup = Popup(
            title=title,
            content=prompt,
            size_hint=(0.8, 0.6),
            auto_dismiss=False,
        )

        def on_save(*_args):
            initials = (text.text.strip().upper() or "???")[:NAME_LEN]
            scores = load_scores(self._scores_path)
            scores = record_score(self.board.state.score, initials, scores)
            save_scores(scores, self._scores_path)
            popup.dismiss()
            self.manager.current = "menu"

        ok_btn.bind(on_press=on_save)
        cancel_btn.bind(on_press=lambda *_: popup.dismiss())
        popup.bind(on_dismiss=lambda *_: setattr(self.manager, "current", "menu"))
        popup.open()


class ScoresScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._scores_path = None
        self._label = Label(
            text="", halign="center", valign="middle", color=NEON["white"]
        )

        layout = NeonPanel(orientation="vertical", padding=16, spacing=8)
        layout.add_widget(Label(text="High Scores", font_size=28, color=NEON["white"]))
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
