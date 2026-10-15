def assert_valid_user_response(response):
    data = response.json()
    assert "id" in data
    assert "email" in data


def assert_valid_login_response(response):
    data = response.json()
    assert "access_token" in data
    assert "user_id" in data


def assert_valid_dashboard_response(data):
    assert "theta" in data
    assert "accuracy" in data
    assert "weak_topics" in data
    assert 0 <= data.get("accuracy", 0) <= 1