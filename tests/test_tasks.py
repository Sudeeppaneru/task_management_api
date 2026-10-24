def register_and_login(client, username, email):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "securepassword123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    res = client.post(
        "/api/v1/auth/login/json",
        json={"email": email, "password": "securepassword123"},
    )
    return res.json()["access_token"]


def test_task_crud_and_ownership(client):
    token1 = register_and_login(client, "user1", "user1@example.com")
    token2 = register_and_login(client, "user2", "user2@example.com")

    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Create task as user1
    create_res = client.post(
        "/api/v1/tasks",
        json={"task_description": "First user task", "task_status": "todo"},
        headers=headers1,
    )
    assert create_res.status_code == 201
    task_data = create_res.json()
    task_id = task_data["id"]
    assert task_data["task_status"] == "todo"
    assert task_data["completed_on"] is None

    # Get task as user1
    get_res = client.get(f"/api/v1/tasks/{task_id}", headers=headers1)
    assert get_res.status_code == 200

    # User2 cannot get user1's task (returns 404 for security)
    get_res2 = client.get(f"/api/v1/tasks/{task_id}", headers=headers2)
    assert get_res2.status_code == 404

    # Update task status to completed (should set completed_on)
    patch_res = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"task_status": "completed"},
        headers=headers1,
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["task_status"] == "completed"
    assert patch_res.json()["completed_on"] is not None

    # List tasks
    list_res = client.get("/api/v1/tasks", headers=headers1)
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # Delete task
    del_res = client.delete(f"/api/v1/tasks/{task_id}", headers=headers1)
    assert del_res.status_code == 204

    # Task should not appear in list anymore
    list_res2 = client.get("/api/v1/tasks", headers=headers1)
    assert len(list_res2.json()) == 0
