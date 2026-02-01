"""tests for app:users routes"""


def test_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
