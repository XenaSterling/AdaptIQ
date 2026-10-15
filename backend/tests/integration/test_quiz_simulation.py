from app.services.adaptive_engine import get_next_question
from app.ml.irt.update import update_theta
from app.services.dashboard_service import get_student_dashboard


def test_full_student_learning_simulation(db, test_module):


    questions = []

    for i in range(-2, 3):

        q = get_next_question.__globals__['Question'](
            content=f"Q{i}",
            difficulty=float(i),
            discrimination=1.0,
            module_id=test_module.id
        )

        db.add(q)
        questions.append(q)

    db.commit()

    theta = 0.0
    used = []


    for step in range(5):

        q = get_next_question(db, theta, used)

        assert q is not None

        used.append(q.id)

        correct = step % 2 == 0

        responses = [{
            "correct": correct,
            "difficulty": q.difficulty,
            "discrimination": q.discrimination
        }]

        theta = update_theta(theta, responses)

    assert isinstance(theta, float)

    dashboard = get_student_dashboard(db, test_module.id)

    assert "theta" in dashboard
    assert "accuracy" in dashboard
    assert "weak_topics" in dashboard