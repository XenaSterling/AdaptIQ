from app.services.adaptive_engine import get_next_question


def test_get_next_question_empty_db(db):
    result = get_next_question(db, theta=0.0, used_question_ids=[])
    assert result is None


def test_get_next_question_all_excluded(db, test_module):
    from app.models.question import Question

    q = Question(
        content="Only",
        difficulty=0.0,
        discrimination=1.0,
        module_id=test_module.id
    )

    db.add(q)
    db.commit()

    result = get_next_question(db, theta=0.0, used_question_ids=[q.id])

    assert result is None