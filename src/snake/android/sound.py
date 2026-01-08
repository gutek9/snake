"""Minimal tone generator for arcade-style feedback."""

import os
import struct
import wave

from kivy.clock import Clock
from kivy.core.audio import SoundLoader


class TonePlayer:
    """Generate and play short WAV tones without external assets."""

    def __init__(self, cache_dir, voices=3):
        self._cache_dir = os.path.join(cache_dir, "sounds")
        self._sounds = {}
        self._voice_index = {}
        self._loops = {}
        self._voices = max(1, int(voices))
        os.makedirs(self._cache_dir, exist_ok=True)

    def play(self, name, freq, duration_ms, volume=0.6):
        """Play a single tone with simple polyphony support."""
        key = f"{name}_{int(freq)}_{int(duration_ms)}"
        voices = self._sounds.get(key)
        if voices is None:
            path = self._tone_path(name, freq, duration_ms)
            if not os.path.exists(path):
                _write_tone(path, freq, duration_ms)
            voices = []
            for _ in range(self._voices):
                sound = SoundLoader.load(path)
                if sound is not None:
                    voices.append(sound)
            if not voices:
                return
            self._sounds[key] = voices
            self._voice_index[key] = 0
        idx = self._voice_index[key]
        self._voice_index[key] = (idx + 1) % len(voices)
        sound = voices[idx]
        sound.volume = volume
        sound.play()

    def play_chord(self, name, freqs, duration_ms, volume=0.6):
        """Play multiple tones at once to imitate phone polyphony."""
        for freq in freqs:
            self.play(f"{name}_{int(freq)}", freq, duration_ms, volume=volume)

    def play_sequence(self, name, sequence, loop=False):
        """Schedule a sequence of tones; optionally loop it."""
        handle = {"active": True, "events": [], "name": name}

        def schedule_from(offset_ms):
            for step in sequence:
                freqs, duration_ms, volume = step
                event = Clock.schedule_once(
                    lambda _dt, f=freqs, d=duration_ms, v=volume: self._play_step(
                        name, f, d, v, handle
                    ),
                    offset_ms / 1000.0,
                )
                handle["events"].append(event)
                offset_ms += duration_ms
            if loop:
                loop_event = Clock.schedule_once(
                    lambda _dt: schedule_from(0), offset_ms / 1000.0
                )
                handle["events"].append(loop_event)

        schedule_from(0)
        self._loops[name] = handle
        return handle

    def stop_sequence(self, name):
        """Stop a previously scheduled sequence."""
        handle = self._loops.pop(name, None)
        if handle is None:
            return
        handle["active"] = False
        for event in handle["events"]:
            event.cancel()

    def _play_step(self, name, freqs, duration_ms, volume, handle):
        if not handle.get("active"):
            return
        if isinstance(freqs, (list, tuple)):
            self.play_chord(name, freqs, duration_ms, volume=volume)
        else:
            self.play(name, freqs, duration_ms, volume=volume)

    def _tone_path(self, name, freq, duration_ms):
        return os.path.join(
            self._cache_dir, f"{name}_{int(freq)}_{int(duration_ms)}.wav"
        )


def _write_tone(path, freq, duration_ms, sample_rate=22050):
    frames = int(sample_rate * (duration_ms / 1000.0))
    amplitude = 32767
    with wave.open(path, "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        for i in range(frames):
            value = int(amplitude * 0.5 * _sine(2.0 * 3.14159265 * freq * i / sample_rate))
            handle.writeframes(struct.pack("<h", value))


def _sine(x):
    return __import__("math").sin(x)


class MusicPlayer:
    """Simple wrapper around Kivy SoundLoader for looping music."""

    def __init__(self):
        self._current = None

    def load(self, path):
        sound = SoundLoader.load(path)
        if sound is None:
            return None
        sound.loop = True
        return sound

    def play(self, sound):
        self.stop()
        if sound is None:
            return
        self._current = sound
        self._current.play()

    def stop(self):
        if self._current is None:
            return
        self._current.stop()
        self._current = None
