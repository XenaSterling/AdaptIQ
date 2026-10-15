import uuid


def test_complete_user_flow(client):

    email = f"{uuid.uuid4()}@test.com"

    # REGISTER
    r = client.post("/auth/register", json={
        "name": "E2E User",
        "email": email,
        "password": "123456"
    })
    assert r.status_code == 200

    # LOGIN
    r = client.post("/auth/login", json={
        "email": email,
        "password": "123456"
    })
    assert r.status_code == 200

    data = r.json()

    assert "access_token" in data
    assert "user_id" in data

    user_id = data["user_id"]

    # DASHBOARD
    r = client.get(f"/dashboard/student/{user_id}")
    assert r.status_code == 200