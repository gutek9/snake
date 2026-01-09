import json

from snake.scores_store import load_scores, record_score, reset_scores, save_scores


def test_load_scores_returns_empty_when_missing(tmp_path):
    missing = tmp_path / "scores.json"
    scores = load_scores(str(missing))
    assert scores == []


def test_record_score_keeps_top_scores():
    scores = []
    scores = record_score(10, "AAA", scores)
    scores = record_score(5, "BBB", scores)
    scores = record_score(20, "CCC", scores)
    assert scores[0]["score"] == 20
    assert scores[1]["score"] == 10
    assert scores[2]["score"] == 5


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "scores.json"
    data = [{"name": "AAA", "score": 12}]
    save_scores(data, str(path))
    loaded = load_scores(str(path))
    assert loaded == data


def test_reset_scores_overwrites_file(tmp_path):
    path = tmp_path / "scores.json"
    path.write_text(json.dumps([{"name": "AAA", "score": 12}]), encoding="utf-8")
    reset_scores(str(path))
    loaded = load_scores(str(path))
    assert loaded == []
