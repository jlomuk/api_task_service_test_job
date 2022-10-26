from fastapi.testclient import TestClient

URL = '/api/v1/task/'


def test_create_with_correct_data(test_client: TestClient):
    data = {
        'title': 'TestTitle',
        'completed': False,
        'user_id': 1,
        'username': 'TestUser',
    }
    result = test_client.post(URL, json=data)
    assert result.status_code == 201
    assert result.json() == data | {'id': 1}


def test_create_task_without_completed_status(test_client: TestClient):
    data = {
        'title': 'TestTitle',
        'user_id': 1,
        'username': 'TestUser',
    }
    result = test_client.post(URL, json=data)
    assert result.status_code == 201
    assert result.json()['completed'] == 0


def test_create_with_wrong_data(test_client: TestClient):
    result = test_client.post(URL, json={'wrong_data': 'dummy', 'username': 'TestUser'})
    assert result.status_code == 422
