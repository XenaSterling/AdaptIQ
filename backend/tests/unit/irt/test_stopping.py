from app.ml.cat.stopping import should_stop_evaluation

from types import SimpleNamespace

def make_settings():
    return SimpleNamespace(
        min_questions=3,
        max_questions=10,
        max_uncertainty=0.5,
        use_uncertainty_stop=True,
        stability_window=3,
        theta_stability_threshold=0.5
    )

def test_should_stop_insufficient_data():

    result = should_stop_evaluation(
        session_state={"used": []},
        settings=make_settings(),
        theta_history=[0.0],
        uncertainty=1.0,
        questions_answered=0
    )

    assert isinstance(result, dict)
    assert "stop" in result


def test_should_stop_after_min_questions():

    result = should_stop_evaluation(
        session_state={"used": [1, 2, 3, 4, 5]},
        settings=make_settings(),
        theta_history=[0.0] * 6,
        uncertainty=0.2,
        questions_answered=5
    )

    assert isinstance(result, dict)