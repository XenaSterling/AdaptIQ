import pytest


def test_register_duplicate_email(client):

    email = "duplicate@test.com"

    r1 = client.post("/auth/register", json={
        "name": "A",
        "email": email,
        "password": "1234"
    })

    assert r1.status_code == 200

    r2 = client.post("/auth/register", json={
        "name": "B",
        "email": email,
        "password": "1234"
    })

    assert r2.status_code == 400