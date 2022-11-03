from fastapi.testclient import TestClient

URL = '/api/v1/task'


def test_delete_correct_task(test_client: TestClient, create_fake_data: int):
    user_id, task_id = create_fake_data, 1
    result = test_client.delete(f'{URL}/{task_id}', params={'user_id': user_id})
    assert result.status_code == 204

    check_response = test_client.get(f'{URL}/{task_id}', params={'user_id': user_id})
    assert len(check_response.json()) == 1


def test_delete_not_correct_task(test_client: TestClient, create_fake_data: int):
    user_id = create_fake_data
    result = test_client.delete(f'{URL}/{9999}', params={'user_id': user_id})
    assert result.status_code == 404


def test_delete_correct_task_another_user(test_client: TestClient, create_fake_data: int):
    user_id = 999
    result = test_client.delete(f'{URL}/{1}', params={'user_id': user_id})
    assert result.status_code == 404
