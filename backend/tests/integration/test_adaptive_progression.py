from app.services.adaptive_engine import get_next_question


def test_difficulty_adapts_to_theta(db, test_module):

    easy = []
    hard = []

    for i in range(-3, 4):

        q = get_next_question.__globals__['Question'](
            content=f"Q{i}",
            difficulty=float(i),
            discrimination=1.0,
            module_id=test_module.id
        )

        db.add(q)

    db.commit()

    # =====================================================
    # LOW THETA
    # =====================================================

    q1 = get_next_question(db, -2.0, [])

    assert q1 is not None
    easy.append(q1.difficulty)

    # =====================================================
    # HIGH THETA
    # =====================================================

    q2 = get_next_question(db, 2.0, [])

    assert q2 is not None
    hard.append(q2.difficulty)

    # =====================================================
    # ASSERT BEHAVIOR CHANGE
    # =====================================================

    assert q1.difficulty <= q2.difficulty