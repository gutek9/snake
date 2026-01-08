"""Shared score storage for all front ends."""

import json
import os

DEFAULT_PATH = os.path.join(
    os.path.expanduser("~"), ".terminal_snake_scores.json"
)
MAX_SCORES = 10
NAME_LEN = 3


def load_scores(path=DEFAULT_PATH):
    """Load scores from disk; return an empty list on failure."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        scores = []
        for item in data:
            if isinstance(item, dict):
                name = str(item.get("name", "???"))[:NAME_LEN]
                score = int(item.get("score", 0))
                scores.append({"name": name, "score": score})
            else:
                scores.append({"name": "???", "score": int(item)})
        return sorted(scores, key=lambda row: row["score"], reverse=True)[
            :MAX_SCORES
        ]
    except (OSError, ValueError, TypeError):
        return []


def save_scores(scores, path=DEFAULT_PATH):
    """Persist scores to disk, best-effort."""
    try:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(scores, handle)
    except OSError:
        return False
    return True


def record_score(score, name, scores):
    """Insert a new score into the list and keep the top 10."""
    updated = list(scores)
    if score is not None:
        updated.append({"name": name or "???", "score": int(score)})
    updated = sorted(updated, key=lambda row: row["score"], reverse=True)[
        :MAX_SCORES
    ]
    return updated


def default_scores_path():
    """Return the default score file path for terminal installs."""
    return DEFAULT_PATH
