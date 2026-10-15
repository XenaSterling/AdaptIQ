from app.ml.recommender.recommender_engine import recommend_hybrid
from app.models.question import Question


def test_recommender_changes_with_learning(
    db,
    test_module,
    test_user
):


    for i in range(-3, 4):

        q = Question(
            content=f"Q{i}",
            difficulty=float(i),
            discrimination=1.0,
            module_id=test_module.id
        )

        db.add(q)

    db.commit()

    recs1 = recommend_hybrid(
        db,
        test_user.id,
        0.0,
        3
    )


    recs2 = recommend_hybrid(
        db,
        test_user.id,
        2.0,
        3
    )

    assert len(recs1) <= 3
    assert len(recs2) <= 3

    assert recs1 != recs2