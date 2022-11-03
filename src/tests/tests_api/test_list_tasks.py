from fastapi.testclient import TestClient

URL = '/api/v1/task'


def test_get_user_list_tasks(test_client: TestClient, create_fake_data: int):
    user_id = create_fake_data
    result = test_client.get(URL, params={'user_id': user_id})
    assert result.status_code == 200
    assert len(result.json()) == 2


def test_get_list_tasks_for_other_user(test_client: TestClient, create_fake_data: int):
    user_id = 2
    result = test_client.get(URL, params={'user_id': user_id})
    assert result.status_code == 200
    assert len(result.json()) == 0
