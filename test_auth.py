def test_login_success(client):
    response = client.post(
        "/login",
        data={"username": "bhakti", "password": "1234"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client):
    response = client.post(
        "/login",
        data={"username": "bhakti", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()
