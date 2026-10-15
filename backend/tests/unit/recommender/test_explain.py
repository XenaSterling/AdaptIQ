from types import SimpleNamespace

from app.ml.recommender.explain import diversity_penalty


def make_question(tag_ids):

    return SimpleNamespace(
        tags=[
            SimpleNamespace(tag_id=t)
            for t in tag_ids
        ]
    )


def test_diversity_penalty_no_overlap():

    selected = [
        make_question(["math"])
    ]

    candidate = make_question(["history"])

    penalty = diversity_penalty(
        selected,
        candidate
    )

    assert penalty == 1.0


def test_diversity_penalty_with_overlap():

    selected = [
        make_question(["math"])
    ]

    candidate = make_question(["math"])

    penalty = diversity_penalty(
        selected,
        candidate
    )

    assert penalty < 1.0