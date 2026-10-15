from app.ml.irt.model import probability_correct
from app.ml.irt.update import update_theta


def test_probability_correct():

    p = probability_correct(0, 0)
    assert 0.4 < p < 0.6


def test_theta_update_improves_on_correct():

    theta = 0.0

    responses = [
        {
            "correct": True,
            "difficulty": 0.0,
            "discrimination": 1.0
        }
    ]

    new_theta = update_theta(theta, responses)

    assert new_theta > theta


def test_probability_increases_with_theta():

    low = probability_correct(
        theta=-2,
        difficulty=0
    )

    high = probability_correct(
        theta=2,
        difficulty=0
    )

    assert high > low


def test_harder_question_reduces_probability():

    easy = probability_correct(
        theta=0,
        difficulty=-2
    )

    hard = probability_correct(
        theta=0,
        difficulty=2
    )

    assert easy > hard


def test_theta_update_decreases_on_wrong_answer():

    theta = 0.0

    responses = [
        {
            "correct": False,
            "difficulty": 0.0,
            "discrimination": 1.0
        }
    ]

    new_theta = update_theta(
        theta,
        responses
    )

    assert new_theta < theta


def test_theta_improves_after_multiple_correct_answers():

    theta = 0.0

    responses = [
        {
            "correct": True,
            "difficulty": -1.0,
            "discrimination": 1.0
        },
        {
            "correct": True,
            "difficulty": 0.0,
            "discrimination": 1.0
        },
        {
            "correct": True,
            "difficulty": 1.0,
            "discrimination": 1.0
        }
    ]

    new_theta = update_theta(
        theta,
        responses
    )

    assert new_theta > 0.0


def test_probability_is_always_between_zero_and_one():

    p = probability_correct(
        theta=999,
        difficulty=-4
    )

    assert 0 <= p <= 1