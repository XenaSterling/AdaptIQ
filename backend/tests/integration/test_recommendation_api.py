from fastapi.testclient import TestClient

from app.main import app
from app.models.question import Question
from app.models.learning_resource import LearningResource


client = TestClient(app)


def auth_headers(token: str):
    return {
        "Authorization": f"Bearer {token}"
    }


def get_token(client, email="rec_test@test.com"):

    client.post(
        "/auth/register",
        json={
            "name": "rec_test",
            "email": email,
            "password": "1234"
        }
    )

    res = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "1234"
        }
    )

    return res.json()["access_token"]


def test_recommendation_questions_api(db, test_module):

    for i in range(5):

        db.add(
            Question(
                content=f"Q{i}",
                difficulty=float(i),
                discrimination=1.0,
                module_id=test_module.id
            )
        )

    db.commit()

    token = get_token(client)

    response = client.get(
        "/recommendations/questions/me",
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    data = response.json()

    assert "theta" in data
    assert "weak_tags" in data
    assert "recommendations" in data

    assert isinstance(data["recommendations"], list)


def test_recommendation_resources_api(db, test_module):

    for i in range(5):

        db.add(
            LearningResource(
                title=f"R{i}",
                description="desc",
                type="video",
                difficulty=float(i),
                url=f"http://test{i}.com"
            )
        )

    db.commit()

    token = get_token(client)

    response = client.get(
        "/recommendations/resources/me",
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    data = response.json()

    assert "theta" in data
    assert "resources" in data
    assert isinstance(data["resources"], list)


def test_recommendation_dashboard_api(db, test_module):

    for i in range(5):

        db.add(
            Question(
                content=f"Q{i}",
                difficulty=float(i),
                discrimination=1.0,
                module_id=test_module.id
            )
        )

        db.add(
            LearningResource(
                title=f"R{i}",
                description="desc",
                type="video",
                difficulty=float(i),
                url=f"http://test{i}.com"
            )
        )

    db.commit()

    token = get_token(client)

    response = client.get(
        "/recommendations/dashboard/me",
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    data = response.json()

    assert "theta" in data
    assert "weak_tags" in data
    assert "questions" in data
    assert "resources" in data

    assert isinstance(data["questions"], list)
    assert isinstance(data["resources"], list)