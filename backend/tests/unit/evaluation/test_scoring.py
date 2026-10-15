import pytest
from app.services.evaluation_service import compute_score


def test_scoring_perfect_all_correct():
    responses = [
        {"correct": True, "difficulty": 1.0},
        {"correct": True, "difficulty": 1.0},
        {"correct": True, "difficulty": 1.0},
    ]

    score = compute_score(responses)

    assert isinstance(score, float)
    assert score == 10.0


def test_scoring_all_wrong():
    responses = [
        {"correct": False, "difficulty": 1.0},
        {"correct": False, "difficulty": 1.0},
    ]

    score = compute_score(responses)

    assert score == 0.0


def test_scoring_mixed_results():
    responses = [
        {"correct": True, "difficulty": 1.0},
        {"correct": False, "difficulty": 1.0},
        {"correct": True, "difficulty": 1.0},
    ]

    score = compute_score(responses)

    assert 0.0 < score < 10.0