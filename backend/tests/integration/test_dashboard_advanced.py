from app.services.dashboard_service import get_student_dashboard


def test_dashboard_without_ability(db, test_user):
    """
    fuerza rama donde StudentAbility no existe
    """

    result = get_student_dashboard(db, test_user.id)

    assert isinstance(result, dict)
    assert "theta" in result
    assert "accuracy" in result