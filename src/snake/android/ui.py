"""Shared UI widgets for the Android front end."""

import math
import random

from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from .theme import NEON


class NeonButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = NEON["white"]
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
            Color(*NEON["panel"])
            RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
            glow = 0.6 + (self._pulse * 0.4)
            Color(NEON["cyan"][0], NEON["cyan"][1], NEON["cyan"][2], glow)
            Line(
                rounded_rectangle=(
                    self.x + 2,
                    self.y + 2,
                    self.width - 4,
                    self.height - 4,
                    12,
                ),
                width=1.2,
            )


class NeonPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *_args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*NEON["panel"])
            RoundedRectangle(pos=self.pos, size=self.size, radius=[16])
            Color(*NEON["magenta"])
            Line(
                rounded_rectangle=(
                    self.x + 1,
                    self.y + 1,
                    self.width - 2,
                    self.height - 2,
                    16,
                ),
                width=1.0,
            )


class SpaceBackdrop(Widget):
    """Draw a subtle outer-space backdrop behind the HUD."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._stars = []
        self._anim = None
        self.bind(pos=self._redraw, size=self._redraw)
        self._start_animation()

    def _start_animation(self):
        if self._anim is None:
            self._anim = Clock.schedule_interval(self._tick, 1 / 24)

    def start_animation(self):
        self._start_animation()

    def stop_animation(self):
        if self._anim is not None:
            self._anim.cancel()
            self._anim = None

    def _init_stars(self):
        self._stars = []
        for i in range(40):
            self._stars.append(
                {
                    "x": (i * 37) % max(1, int(self.width)),
                    "y": (i * 53) % max(1, int(self.height)),
                    "speed": 6 + (i % 5),
                }
            )

    def _tick(self, _dt):
        if not self._stars:
            self._init_stars()
        for star in self._stars:
            star["y"] -= star["speed"] / 4.0
            if star["y"] < self.y + 4:
                star["y"] = self.top - 4
        self._redraw()

    def _redraw(self, *_args):
        self.canvas.clear()
        with self.canvas:
            Color(0.01, 0.02, 0.04, 1.0)
            Rectangle(pos=self.pos, size=self.size)
            Color(0.8, 0.9, 1.0, 0.3)
            for star in self._stars:
                Line(points=[star["x"], star["y"], star["x"], star["y"]], width=1)
            Color(0.1, 0.4, 0.7, 0.08)
            for i in range(6):
                y = self.y + 10 + i * 24
                Line(points=[self.x + 6, y, self.right - 6, y], width=1)
            Color(0.05, 0.2, 0.35, 0.25)
            Line(
                rectangle=(self.x + 6, self.y + 6, self.width - 12, self.height - 12),
                width=1,
            )
            for i in range(6):
                offset = 18 + i * 26
                Line(
                    points=[
                        self.x + offset,
                        self.y + 4,
                        self.x + offset + 12,
                        self.y + 4,
                    ],
                    width=1,
                )


class TitleOverlay(FloatLayout):
    """ASCII title block for the right side gutter."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self._title = Label(
            text="CODEX\nSNAKE",
            color=NEON["magenta"],
            font_size=36,
            halign="center",
            valign="middle",
        )
        self._title.bind(size=self._title.setter("text_size"))
        self._title.pos_hint = {"center_x": 0.5, "center_y": 0.6}
        self._title.size_hint = (0.95, 0.5)
        self.add_widget(self._title)
        self._glitch = Clock.schedule_interval(self._tick_glitch, 1 / 12)
        self._phase = 0.0

    def start_animation(self):
        if self._glitch is None:
            self._glitch = Clock.schedule_interval(self._tick_glitch, 1 / 12)

    def stop_animation(self):
        if self._glitch is not None:
            self._glitch.cancel()
            self._glitch = None

    def _tick_glitch(self, dt):
        self._phase += dt * 3.0
        if random.random() < 0.12:
            alpha = 0.35
            shift = random.choice([-3, -2, 2, 3])
        else:
            alpha = 0.7 + (math.sin(self._phase) * 0.25)
            shift = 0
        self._title.color = (
            NEON["magenta"][0],
            NEON["magenta"][1],
            NEON["magenta"][2],
            max(0.3, min(1.0, alpha)),
        )
        self._title.x = self.x + shift
