"""Overlay widgets for the Android front end."""

import random

from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from .theme import NEON


class CyberOverlay(FloatLayout):
    """Cyberpunk side readouts to fill space outside the board."""

    def __init__(self, align="left", show_matrix=True, **kwargs):
        super().__init__(**kwargs)
        self._align = align
        self._show_matrix = show_matrix
        self.size_hint = (None, None)
        self._matrix = None
        if self._show_matrix:
            self._matrix = Label(
                text="",
                color=(0.2, 1.0, 0.6, 0.8),
                font_size=18,
                halign="left" if align == "left" else "right",
                valign="top",
            )
            self._matrix.bind(size=self._matrix.setter("text_size"))
            self._matrix.pos_hint = {"center_x": 0.5, "center_y": 0.6}
            self._matrix.size_hint = (0.95, 0.45)
            self.add_widget(self._matrix)

        self._readout = Label(
            text="SYS 88\nSPD 01\nLEN 03\nPWR 77\nSCR 0000\nDIR R",
            color=NEON["cyan"],
            font_size=20,
            halign="left" if align == "left" else "right",
            valign="top",
        )
        self._readout.bind(size=self._readout.setter("text_size"))
        self._readout.pos_hint = {"center_x": 0.5, "center_y": 0.72}
        self._readout.size_hint = (0.95, 0.4)
        self.add_widget(self._readout)

        self._scan = Label(
            text="SYNC: OK" if align == "left" else "LINK: OK",
            color=NEON["magenta"],
            font_size=16,
            halign="center",
        )
        self._scan.pos_hint = {"center_x": 0.5, "center_y": 0.18}
        self._scan.size_hint = (0.9, 0.1)
        self.add_widget(self._scan)

        self._anim = Clock.schedule_interval(self._tick, 1 / 10)
        self._stats_provider = None

    def bind_stats(self, fn):
        self._stats_provider = fn

    def _tick(self, _dt):
        if self._matrix is not None:
            chars = "0123456789ABCDEF"
            lines = []
            for _ in range(6):
                line = "".join(random.choice(chars) for _ in range(14))
                lines.append(line)
            self._matrix.text = "\n".join(lines)
        if self._stats_provider is not None:
            stats = self._stats_provider()
            self._readout.text = (
                f"SYS {stats['sys']:02d}\n"
                f"SPD {stats['spd']:02d}\n"
                f"LEN {stats['len']:02d}\n"
                f"PWR {stats['pwr']:02d}\n"
                f"SCR {stats['scr']:04d}\n"
                f"DIR {stats['dir']}"
            )
