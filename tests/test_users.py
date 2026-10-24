def test_get_and_update_my_profile(client):
    payload = {
        "username": "profileuser",
        "email": "profile@example.com",
        "password": "securepassword123",
        "first_name": "Profile",
        "last_name": "User",
    }
    client.post("/api/v1/auth/register", json=payload)

    login_res = client.post(
        "/api/v1/auth/login/json",
        json={"email": "profile@example.com", "password": "securepassword123"},
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # GET /api/v1/users/me
    res = client.get("/api/v1/users/me", headers=headers)
    assert res.status_code == 200
    assert res.json()["username"] == "profileuser"

    # PATCH /api/v1/users/me
    patch_res = client.patch(
        "/api/v1/users/me",
        json={"first_name": "UpdatedName", "phone_no": "1234567890"},
        headers=headers,
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["first_name"] == "UpdatedName"
    assert patch_res.json()["phone_no"] == "1234567890"
