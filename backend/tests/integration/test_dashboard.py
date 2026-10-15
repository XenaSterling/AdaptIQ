from app.services.dashboard_service import get_student_dashboard
from tests.utils.assertions import assert_valid_dashboard_response

from app.auth.security import hash_password
from app.models.user import User
from app.models.student_ability import StudentAbility
from app.models.role import Role


# =====================================================
# SERVICE TEST
# =====================================================

def test_dashboard_service(db, test_user, test_ability):

    result = get_student_dashboard(db, test_user.id)

    assert_valid_dashboard_response(result)


# =====================================================
# ENDPOINT TEST
# =====================================================

def test_dashboard_endpoint(client, test_user):

    res = client.get(f"/dashboard/student/{test_user.id}")

    assert res.status_code == 200


# =====================================================
# DASHBOARD CORE
# =====================================================

def test_student_dashboard(db, test_user):

    ability = StudentAbility(
        user_id=test_user.id,
        theta=0.5
    )

    db.add(ability)
    db.commit()

    result = get_student_dashboard(db, test_user.id)

    assert "theta" in result
    assert "accuracy" in result
    assert "weak_topics" in result


# =====================================================
# ENDPOINT REFLECTION TEST
# =====================================================

def test_endpoint_student_dashboard(client, test_user, db):

    response = client.get(
        f"/dashboard/student/{test_user.id}"
    )

    assert response.status_code == 200


# =====================================================
# STATE CHANGE TEST
# =====================================================

def test_dashboard_reflects_user_state(db, test_user, test_ability):

    result = get_student_dashboard(db, test_user.id)
    initial_theta = result["theta"]

    test_ability.theta = 2.0
    db.commit()

    result2 = get_student_dashboard(db, test_user.id)

    assert result2["theta"] != initial_theta