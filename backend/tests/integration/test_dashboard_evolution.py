from app.services.dashboard_service import get_student_dashboard
from app.models.student_ability import StudentAbility


def test_dashboard_updates_with_theta(db, test_user):

    ability = StudentAbility(user_id=test_user.id, theta=0.0)
    db.add(ability)
    db.commit()

    d1 = get_student_dashboard(db, test_user.id)

    ability.theta = 3.0
    db.commit()

    d2 = get_student_dashboard(db, test_user.id)

    assert d1["theta"] != d2["theta"]