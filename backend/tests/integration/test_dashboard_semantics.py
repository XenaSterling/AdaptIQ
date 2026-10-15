from app.services.dashboard_service import get_student_dashboard
from app.services.recommendation_service import (
    get_recommendation_dashboard_service
)

from app.models.student_ability import StudentAbility

from tests.utils.factories import create_user


# =====================================================
# DASHBOARD AND RECOMMENDER SHARE THETA
# =====================================================

def test_dashboard_and_recommendations_use_same_theta(
    db
):

    user = create_user(db)

    db.add(
        StudentAbility(
            user_id=user.id,
            theta=1.75
        )
    )

    db.commit()

    dashboard = get_student_dashboard(
        db,
        user.id
    )

    recommendations = (
        get_recommendation_dashboard_service(
            db,
            user.id
        )
    )

    assert dashboard["theta"] == recommendations["theta"]


# =====================================================
# THETA CHANGE PROPAGATES
# =====================================================

def test_theta_change_propagates_to_dashboard_and_recommendations(
    db
):

    user = create_user(db)

    ability = StudentAbility(
        user_id=user.id,
        theta=0.0
    )

    db.add(ability)
    db.commit()

    dashboard_1 = get_student_dashboard(
        db,
        user.id
    )

    recommendations_1 = (
        get_recommendation_dashboard_service(
            db,
            user.id
        )
    )

    ability.theta = 2.5
    db.commit()

    dashboard_2 = get_student_dashboard(
        db,
        user.id
    )

    recommendations_2 = (
        get_recommendation_dashboard_service(
            db,
            user.id
        )
    )

    assert dashboard_1["theta"] != dashboard_2["theta"]

    assert (
        recommendations_1["theta"]
        != recommendations_2["theta"]
    )

    assert (
        dashboard_2["theta"]
        == recommendations_2["theta"]
    )