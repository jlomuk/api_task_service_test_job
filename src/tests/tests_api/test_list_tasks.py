from fastapi.testclient import TestClient

URL = '/api/v1/task'


def test_get_user_list_tasks_(test_client: TestClient, create_fake_data: int):
    user_id = create_fake_data
    result = test_client.get(URL, params={'user_id': user_id})
    print(result.status_code, result.json())
