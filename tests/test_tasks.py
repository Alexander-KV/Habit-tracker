def test_create_task(client):
    response = client.post("/tasks", json={"title": "Learn pytest", "description": "day 4"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Learn pytest"
    assert data["completed"] == False
    assert "id" in data


def test_get_task_not_found(client):
    response = client.get("/tasks/9999")
    assert response.status_code == 404


def test_get_task_by_id(client):
    create_response = client.post("/tasks", json={"title": "Test task", "description": "test"})
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test task"


def test_create_task_missing_title(client):
    response = client.post("/tasks", json={"description": "day 4"})
    assert response.status_code == 422


def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_after_create(client):
    client.post("/tasks", json={"title": "fer", "description": "day 4"})
    client.post("/tasks", json={"title": "ber", "description": "day 41"})

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_task(client):
    create_response = client.post("/tasks", json={"title": "Learn pytest", "description": "day 4"})
    task_id = create_response.json()["id"]

    update_response = client.put(f"/tasks/{task_id}", json={"title": "Learn FastAPI", "description": "day 5"})
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Learn FastAPI"

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.json()["title"] == "Learn FastAPI"


def test_update_task_not_found(client):
    response = client.put("/tasks/9999", json={"title": "X", "description": "Y"})
    assert response.status_code == 404


def test_delete_task(client):
    create_response = client.post("/tasks", json={"title": "Learn pytest", "description": "day 4"})
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/tasks/9999")
    assert response.status_code == 404