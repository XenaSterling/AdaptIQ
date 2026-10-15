import uuid


def test_complete_user_flow(client):

    email = f"{uuid.uuid4()}@test.com"

    # =====================================================
    # REGISTER
    # =====================================================

    register_response = client.post(
        "/auth/register",
        json={
            "name": "E2E User",
            "email": email,
            "password": "123456"
        }
    )

    assert register_response.status_code == 200

    # =====================================================
    # LOGIN
    # =====================================================

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,          # ✅ FIX
            "password": "123456"
        }
    )

    assert login_response.status_code == 200

    login_data = login_response.json()

    assert "access_token" in login_data

    user_id = login_data.get("user_id")

    if user_id:

        dashboard_response = client.get(
            f"/dashboard/student/{user_id}"
        )

        assert dashboard_response.status_code == 200


def test_register_login_dashboard_flow(client):

    email = f"{uuid.uuid4()}@test.com"

    # =====================================================
    # REGISTER (FIX: json, no data)
    # =====================================================

    register_res = client.post(
        "/auth/register",
        json={
            "name": "E2E",
            "email": email,
            "password": "123"
        }
    )

    assert register_res.status_code == 200

    # =====================================================
    # LOGIN (FIX: email, no username + json)
    # =====================================================

    login = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "123"
        }
    )

    assert login.status_code == 200

    user_id = login.json().get("user_id")

    if user_id:

        res = client.get(f"/dashboard/student/{user_id}")

        assert res.status_code == 200