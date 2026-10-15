from tests.utils.auth_helpers import register_user, login_user
from tests.utils.assertions import assert_valid_login_response
from app.services.adaptive_engine import get_next_question
from app.ml.irt.update import update_theta
from app.models.question import Question


def test_complete_learning_flow(client):

    email = "e2e@test.com"

    r = register_user(client, email)
    assert r.status_code == 200

    r = login_user(client, email)
    assert r.status_code == 200

    assert_valid_login_response(r)

    user_id = r.json()["user_id"]

    res = client.get(f"/dashboard/student/{user_id}")

    assert res.status_code == 200


def test_full_learning_cycle(db, test_module, test_question, test_user):

    q = Question(
        content="Test Question",
        difficulty=0.0,
        discrimination=1.0,
        module_id=test_module.id
    )

    db.add(q)
    db.commit()
    db.refresh(q)

    theta = 0.0

    # 1. obtener pregunta
    q = get_next_question(db, theta, [])

    assert q is not None

    # 2. simular respuesta correcta
    responses = [{
        "correct": True,
        "difficulty": q.difficulty,
        "discrimination": q.discrimination
    }]

    new_theta = update_theta(theta, responses)

    assert new_theta != theta

    # 3. siguiente pregunta debería adaptarse
    q2 = get_next_question(db, new_theta, [q.id])

    assert q2 is not None