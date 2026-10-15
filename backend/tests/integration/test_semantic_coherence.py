from app.services.evaluation_service import (
    compute_score
)

from app.ml.irt.update import update_theta


def test_theta_and_score_increase_together():

    responses = [
        {
            "correct": True,
            "difficulty": 1.0,
            "discrimination": 1.0
        },
        {
            "correct": True,
            "difficulty": 1.0,
            "discrimination": 1.0
        },
        {
            "correct": True,
            "difficulty": 1.0,
            "discrimination": 1.0
        }
    ]

    theta = update_theta(
        theta=0.0,
        responses=responses
    )

    score = compute_score(
        responses
    )

    assert theta > 0
    assert score >= 8


def test_theta_and_score_decrease_together():

    responses = [
        {
            "correct": False,
            "difficulty": 1.0,
            "discrimination": 1.0
        },
        {
            "correct": False,
            "difficulty": 1.0,
            "discrimination": 1.0
        },
        {
            "correct": False,
            "difficulty": 1.0,
            "discrimination": 1.0
        }
    ]

    theta = update_theta(
        theta=0.0,
        responses=responses
    )

    score = compute_score(
        responses
    )

    assert theta < 0
    assert score <= 2


def test_high_theta_cannot_produce_low_score():

    responses = [
        {
            "correct": True,
            "difficulty": 2.0,
            "discrimination": 1.5
        },
        {
            "correct": True,
            "difficulty": 2.0,
            "discrimination": 1.5
        },
        {
            "correct": True,
            "difficulty": 2.0,
            "discrimination": 1.5
        }
    ]

    theta = update_theta(
        theta=0.0,
        responses=responses
    )

    score = compute_score(
        responses
    )

    assert theta > 0
    assert score > 7


def test_low_theta_cannot_produce_high_score():

    responses = [
        {
            "correct": False,
            "difficulty": 2.0,
            "discrimination": 1.5
        },
        {
            "correct": False,
            "difficulty": 2.0,
            "discrimination": 1.5
        },
        {
            "correct": False,
            "difficulty": 2.0,
            "discrimination": 1.5
        }
    ]

    theta = update_theta(
        theta=0.0,
        responses=responses
    )

    score = compute_score(
        responses
    )

    assert theta < 0
    assert score < 3