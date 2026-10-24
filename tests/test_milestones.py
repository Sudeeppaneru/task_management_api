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


def test_milestone_crud_and_completion(client):
    token = register_and_login(client, "muser", "muser@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Create parent task
    task_res = client.post(
        "/api/v1/tasks",
        json={"task_description": "Parent task for milestones"},
        headers=headers,
    )
    task_id = task_res.json()["id"]

    # Create milestone
    ms_res = client.post(
        f"/api/v1/tasks/{task_id}/milestones",
        json={"milestone_description": "First milestone"},
        headers=headers,
    )
    assert ms_res.status_code == 201
    ms_data = ms_res.json()
    ms_id = ms_data["id"]
    assert ms_data["completed_on"] is None

    # Complete milestone
    comp_res = client.post(
        f"/api/v1/tasks/{task_id}/milestones/{ms_id}/complete",
        headers=headers,
    )
    assert comp_res.status_code == 200
    assert comp_res.json()["completed_on"] is not None

    # List milestones
    list_res = client.get(f"/api/v1/tasks/{task_id}/milestones", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # Delete milestone
    del_res = client.delete(f"/api/v1/tasks/{task_id}/milestones/{ms_id}", headers=headers)
    assert del_res.status_code == 204

    # List should be empty
    list_res2 = client.get(f"/api/v1/tasks/{task_id}/milestones", headers=headers)
    assert len(list_res2.json()) == 0
