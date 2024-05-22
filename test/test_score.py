from datetime import datetime
from score import Score

tmp_path = "data/results.txt"


def test_score_init():
    score = Score("Jack", "70%")
    assert score.name == "Jack"
    assert score.score == "70%"
    assert score.date == datetime.now().strftime("%Y-%m-%d")
    assert score.time == datetime.now().strftime("%H:%M:%S")


def test_score_str():
    score = Score("Jack", "70%")
    assert (
        str(score)
        == f"Name: Jack, Score: 70%, Date: {datetime.now().strftime('%Y-%m-%d')}, Time: {datetime.now().strftime('%H:%M:%S')}"
    )
