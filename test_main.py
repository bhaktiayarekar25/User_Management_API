# from fastapi.testclient import TestClient
# from app import app

# # Test 1: Root endpoint
# def test_root():
#     with TestClient(app) as client:
#         response = client.get("/")
#         assert response.status_code == 200
#         assert response.json() == {"message": "API is working"}

# # Test 2: Admin login + user signup
# def test_register():
#     with TestClient(app) as client:  # ensures database.connect() runs
#         # Step 1: Login as admin
#         login_response = client.post(
#             "/login",
#             data={"username": "bhakti", "password": "1234"}
#         )
#         assert login_response.status_code == 200

#         token = login_response.json()["access_token"]
#         headers = {"Authorization": f"Bearer {token}"}

#         # Step 2: Create a new user
#         response = client.post(
#             "/signup",
#             json={
#                 "username": "sahil",
#                 "email": "sahil@gmail.com",
#                 "password": "1302",
#                 "role": "user"
#             },
#             headers=headers
#         )
#         assert response.status_code in (200, 201)
