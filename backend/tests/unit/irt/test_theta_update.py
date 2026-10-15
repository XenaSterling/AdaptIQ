from app.ml.irt.update import update_theta


def test_theta_increases_on_correct_answer():

    responses = [
        {"correct": True, "difficulty": 0.0, "discrimination": 1.0}
    ]

    theta = update_theta(0.0, responses)

    assert isinstance(theta, float)


def test_theta_decreases_on_wrong_answer():

    responses = [
        {"correct": False, "difficulty": 0.0, "discrimination": 1.0}
    ]

    theta = update_theta(0.0, responses)

    assert isinstance(theta, float)


def test_theta_multiple_responses():

    responses = [
        {"correct": True, "difficulty": -1.0, "discrimination": 1.0},
        {"correct": False, "difficulty": 1.0, "discrimination": 1.0},
        {"correct": True, "difficulty": 0.5, "discrimination": 1.0},
    ]

    theta = update_theta(0.0, responses)

    assert isinstance(theta, float)