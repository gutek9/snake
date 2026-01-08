"""Audio orchestration for the Android front end."""

import os

from .sound import MusicPlayer, TonePlayer


class AndroidAudio:
    """Handle music and SFX with a single interface."""

    def __init__(self, user_data_dir, assets_dir):
        self._tones = TonePlayer(user_data_dir)
        self._music = MusicPlayer()
        self._menu_track = self._music.load(os.path.join(assets_dir, "main_menu.wav"))
        self._game_track = self._music.load(os.path.join(assets_dir, "gameplay.wav"))

    def play_menu(self):
        self._music.play(self._menu_track)

    def play_game(self):
        self._music.play(self._game_track)

    def stop_music(self):
        self._music.stop()

    def play_turn(self):
        self._tones.play("turn", 520, 50, volume=0.5)

    def play_eat(self):
        self._tones.play("eat", 880, 70, volume=0.7)

    def play_game_over(self):
        self._tones.play("game_over", 220, 180, volume=0.8)

    def play_win(self):
        self._tones.play("win", 660, 180, volume=0.8)
        self._tones.play_chord("win_chord", [660, 825, 990], 160, volume=0.6)

    def play_high_score(self):
        self._tones.play_sequence(
            "high_score",
            [
                ([880, 1100], 80, 0.7),
                ([990, 1320], 80, 0.7),
                ([1175, 1568], 120, 0.7),
            ],
        )
