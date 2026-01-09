"""Kivy application bootstrap for the Android front end."""

import os

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from ..scores_store import reset_scores
from .screens import GameScreen, MenuScreen, ScoresScreen
from .sound import TonePlayer
from .theme import NEON


class SnakeApp(App):
    def build(self):
        Window.clearcolor = NEON["bg"]
        scores_path = os.path.join(self.user_data_dir, "scores.json")
        self._audio = TonePlayer(self.user_data_dir)
        _reset_marker = os.path.join(self.user_data_dir, ".scores_reset_v1")
        if not os.path.exists(_reset_marker):
            reset_scores(scores_path)
            with open(_reset_marker, "w", encoding="utf-8") as handle:
                handle.write("ok")

        sm = ScreenManager()
        menu = MenuScreen(name="menu")
        game = GameScreen(name="game")
        scores = ScoresScreen(name="scores")

        game.set_scores_path(scores_path)
        scores.set_scores_path(scores_path)
        game.set_audio(self._audio)

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
