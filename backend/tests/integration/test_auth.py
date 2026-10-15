from tests.utils.auth_helpers import register_user, login_user
from tests.utils.assertions import assert_valid_login_response


def test_register_and_login(client):

    email = "test@test.com"

    r = register_user(client, email)
    assert r.status_code == 200

    r = login_user(client, email)
    assert r.status_code == 200

    assert_valid_login_response(r)