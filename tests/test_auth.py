def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data


def test_register_duplicate_username_and_email(client):
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User",
    }
    res1 = client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    # Duplicate username
    res2 = client.post(
        "/api/v1/auth/register",
        json={**payload, "email": "other@example.com"},
    )
    assert res2.status_code == 409

    # Duplicate email
    res3 = client.post(
        "/api/v1/auth/register",
        json={**payload, "username": "otheruser"},
    )
    assert res3.status_code == 409


def test_login_success_and_failure(client):
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User",
    }
    client.post("/api/v1/auth/register", json=payload)

    # Success login with JSON
    res = client.post(
        "/api/v1/auth/login/json",
        json={"email": "test@example.com", "password": "securepassword123"},
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Failure login with wrong password
    res_fail = client.post(
        "/api/v1/auth/login/json",
        json={"email": "test@example.com", "password": "wrongpassword"},
    )
    assert res_fail.status_code == 401
