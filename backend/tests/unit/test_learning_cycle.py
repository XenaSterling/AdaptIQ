import uuid

from app.services.adaptive_engine import get_next_question
from app.ml.irt.update import update_theta
from app.models.question import Question


def test_full_learning_cycle(db, test_module, test_user):
    """
    Simula aprendizaje completo:
    - preguntas
    - selección adaptativa
    - actualización theta
    """

    q1 = Question(content="Q1", difficulty=-1.0, discrimination=1.0, module_id=test_module.id)
    q2 = Question(content="Q2", difficulty=0.0, discrimination=1.0, module_id=test_module.id)
    q3 = Question(content="Q3", difficulty=1.0, discrimination=1.0, module_id=test_module.id)

    db.add_all([q1, q2, q3])
    db.commit()

    theta = 0.0
    used = []

    q = get_next_question(db, theta, used_question_ids=used)

    assert q is not None
    used.append(q.id)

    responses = [{
        "correct": True,
        "difficulty": q.difficulty,
        "discrimination": q.discrimination
    }]

    new_theta = update_theta(theta, responses)

    assert new_theta != theta

    q_next = get_next_question(db, new_theta, used_question_ids=used)

    assert q_next is not None