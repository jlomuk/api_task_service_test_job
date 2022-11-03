from fastapi.testclient import TestClient

URL = '/api/v1/task'


def test_get_correct_task(test_client: TestClient, create_fake_data: int):
    user_id, task_id = create_fake_data, 1
    result = test_client.get(f'{URL}/{task_id}', params={'user_id': user_id})
    assert result.status_code == 200
    assert result.json()['id'] == task_id


def test_get_not_correct_task(test_client: TestClient, create_fake_data: int):
    user_id = create_fake_data
    result = test_client.get(f'{URL}/{999}', params={'user_id': user_id})
    assert result.status_code == 404


def test_get_correct_task_another_user(test_client: TestClient, create_fake_data: int):
    user_id = 2
    result = test_client.get(f'{URL}/{1}', params={'user_id': user_id})
    assert result.status_code == 404
