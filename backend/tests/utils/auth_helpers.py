def register_user(client, email):
    return client.post(
        "/auth/register",
        json={
            "name": "test",
            "email": email,
            "password": "1234"
        }
    )


def login_user(client, email):
    return client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "1234"
        }
    )