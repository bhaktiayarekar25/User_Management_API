import time

def test_create_user(client):
    # Step 1: Login to get token
    login_res = client.post("/login", data={"username": "bhakti", "password": "1234"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Step 2: Create unique username
    username = f"pytest_user_{int(time.time())}"

    # Step 3: Create user
    res = client.post(
        "/signup",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "pass123",
            "role": "user"
        },
        headers=headers
    )

    print("🔍 Response:", res.json())  # Debug output
    assert res.status_code in (200, 201)


def test_get_users(client):
    # Step 1: Login to get token
    login_res = client.post("/login", data={"username": "bhakti", "password": "1234"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 2: Fetch users
    res = client.get("/users", headers=headers)
    assert res.status_code == 200

    users = res.json()
    assert isinstance(users, list)
    print(f"✅ Total users fetched: {len(users)}")
