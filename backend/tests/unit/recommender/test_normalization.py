from app.ml.recommender.normalization import normalize


def test_normalize_scores():

    scores = {
        "a": 10,
        "b": 20,
        "c": 30
    }

    normalized = normalize(scores)

    assert normalized["a"] == 0.0
    assert normalized["b"] == 0.5
    assert normalized["c"] == 1.0


def test_normalize_empty():

    assert normalize({}) == {}


def test_normalize_same_values():

    scores = {
        "a": 5,
        "b": 5
    }

    normalized = normalize(scores)

    assert normalized["a"] == 0.0
    assert normalized["b"] == 0.0