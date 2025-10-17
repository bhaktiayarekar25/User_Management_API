# import os
# import io
# from fastapi.testclient import TestClient
# from app import app

# client = TestClient(app)

# def test_file_upload():
#     """
#     Test uploading a profile picture (image file) for an authenticated user.
#     """
#     # Step 1: Login to get JWT token
#     login_res = client.post(
#         "/login",
#         data={"username": "bhakti", "password": "1234"}
#     )
#     assert login_res.status_code == 200, "❌ Login failed, cannot continue"
#     token = login_res.json()["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}

#     # Step 2: Create a dummy image (in-memory)
#     sample_image = io.BytesIO()
#     sample_image.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')
#     sample_image.seek(0)

#     # Step 3: Upload file
#     files = {"file": ("profile.png", sample_image, "image/png")}
#     response = client.post("/users/me/upload", headers=headers, files=files)

#     # Step 4: Validate response
#     print("📤 Upload response:", response.json())
#     assert response.status_code in (200, 201), f"Unexpected status: {response.status_code}"

#     data = response.json()
#     assert "filename" in data or "detail" in data


# def test_upload_without_file():
#     """
#     Test upload endpoint when no file is provided (should handle gracefully).
#     """
#     login_res = client.post(
#         "/login",
#         data={"username": "bhakti", "password": "1234"}
#     )
#     assert login_res.status_code == 200
#     token = login_res.json()["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}

#     # Call upload API with no file
#     response = client.post("/users/me/upload", headers=headers, files={})
#     print("🚫 Upload without file:", response.json())

#     # The API should return 400 or 422 with a meaningful message
#     assert response.status_code in (400, 422)
#     assert "detail" in response.json()
# import os
# import io
# from fastapi.testclient import TestClient
# from app import app

# client = TestClient(app)

# def test_file_upload():
#     """
#     Test uploading a profile picture (image file) for an authenticated user.
#     """
#     # Step 1: Login to get JWT token
#     login_res = client.post(
#         "/login",
#         data={"username": "bhakti", "password": "1234"}
#     )
#     assert login_res.status_code == 200, "❌ Login failed, cannot continue"
#     token = login_res.json()["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}

#     # Step 2: Create a dummy image (in-memory)
#     sample_image = io.BytesIO()
#     sample_image.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')
#     sample_image.seek(0)

#     # Step 3: Upload file
#     files = {"file": ("profile.png", sample_image, "image/png")}
#     response = client.post("/users/me/upload", headers=headers, files=files)

#     # Step 4: Validate response
#     print("📤 Upload response:", response.json())
#     assert response.status_code in (200, 201), f"Unexpected status: {response.status_code}"

#     data = response.json()
#     assert "filename" in data or "detail" in data


# def test_upload_without_file():
#     """
#     Test upload endpoint when no file is provided (should handle gracefully).
#     """
#     login_res = client.post(
#         "/login",
#         data={"username": "bhakti", "password": "1234"}
#     )
#     assert login_res.status_code == 200
#     token = login_res.json()["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}

#     # Call upload API with no file
#     response = client.post("/users/me/upload", headers=headers, files={})
#     print("🚫 Upload without file:", response.json())

#     # The API should return 400 or 422 with a meaningful message
#     assert response.status_code in (400, 422)
#     assert "detail" in response.json()
