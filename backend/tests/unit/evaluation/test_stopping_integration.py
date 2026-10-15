from app.ml.cat.stopping import should_stop_evaluation


class FakeSettings:

    def __init__(self):
        self.min_questions = 2
        self.max_questions = 5
        self.use_uncertainty_stop = True
        self.max_uncertainty = 0.2
        self.stability_window = 2
        self.theta_stability_threshold = 0.1


def test_min_questions_blocks_stop():

    settings = FakeSettings()

    result = should_stop_evaluation(
        session_state={},
        settings=settings,
        theta_history=[0.0],
        uncertainty=0.5,
        questions_answered=1
    )

    assert result["stop"] is False


def test_max_questions_forces_stop():

    settings = FakeSettings()

    result = should_stop_evaluation(
        session_state={},
        settings=settings,
        theta_history=[0.0],
        uncertainty=0.5,
        questions_answered=5
    )

    assert result["stop"] is True


def test_uncertainty_triggers_stop():

    settings = FakeSettings()

    result = should_stop_evaluation(
        session_state={},
        settings=settings,
        theta_history=[0.0, 0.1, 0.2],
        uncertainty=0.1,
        questions_answered=3
    )

    assert "reason" in result


def test_theta_stability_detected():

    settings = FakeSettings()

    result = should_stop_evaluation(
        session_state={},
        settings=settings,
        theta_history=[0.1, 0.1, 0.1, 0.1],
        uncertainty=0.1,
        questions_answered=4
    )

    assert "reason" in result