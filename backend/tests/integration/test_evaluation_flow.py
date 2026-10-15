from fastapi.testclient import TestClient
from app.main import app
from app.db.deps import get_db
from app.services.evaluation_service import compute_score
from app.models.module import Module
from app.models.question import Question
from app.models.answer import Answer
import pytest


@pytest.fixture
def client_with_db(db):
    def _get_test_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def build_question(db, module, correct=True):
    q = Question(
        content="Q1",
        difficulty=0.0,
        discrimination=1.0,
        module_id=module.id
    )
    db.add(q)
    db.commit()
    db.refresh(q)

    a1 = Answer(
        question_id=q.id,
        content="A1",
        is_correct=correct
    )
    a2 = Answer(
        question_id=q.id,
        content="A2",
        is_correct=False
    )

    db.add_all([a1, a2])
    db.commit()

    return q


def test_full_cat_evaluation_flow(db, client_with_db, test_user, test_course):

    module = Module(
        title="M1",
        order_index=1,
        course_id=test_course.id
    )
    db.add(module)
    db.commit()
    db.refresh(module)

    q1 = build_question(db, module, correct=True)
    q2 = build_question(db, module, correct=True)

    res = client_with_db.get(
        f"/evaluation/start/{test_user.id}?course_id={test_course.id}"
    )

    assert res.status_code == 200
    data = res.json()

    evaluation_id = data["evaluation_id"]
    question = data["question"]

    assert evaluation_id is not None
    assert question is not None

    for _ in range(2):

        res = client_with_db.post(
            f"/evaluation/answer/{test_user.id}?question_id={question['id']}",
            json={
                "selected_answer_ids": [question["answers"][0]["id"]],
                "response_time": 5
            }
        )

        assert res.status_code == 200
        data = res.json()

        assert "theta" in data

        if data.get("finished"):
            assert "score" in data
            assert "feedback" in data
            break

        assert data["question"] is not None
        question = data["question"]


def test_score_computation_consistency():

    responses = [
        {"correct": True, "difficulty": 1.0, "discrimination": 1.0},
        {"correct": True, "difficulty": 1.0, "discrimination": 1.0},
    ]

    score = compute_score(responses)

    assert 0 <= score <= 10