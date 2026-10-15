from app.models.answer import Answer


def test_user_persistence(db, test_user):

    loaded = db.query(type(test_user)).filter_by(id=test_user.id).first()

    assert loaded is not None


def test_question_answer_persistence(db, test_question):

    a = Answer(
        content="A",
        is_correct=True,
        question_id=test_question.id
    )

    db.add(a)
    db.commit()

    db.expire_all()

    q = db.query(type(test_question)).filter_by(id=test_question.id).first()

    assert len(q.answers) == 1


def test_answer_relationship(db, test_question):

    a = Answer(content="A", is_correct=True, question_id=test_question.id)

    db.add(a)
    db.commit()

    db.expire_all()

    q = db.query(type(test_question)).filter_by(id=test_question.id).first()

    assert q.answers[0].content == "A"