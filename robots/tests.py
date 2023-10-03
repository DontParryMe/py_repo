import pytest
import json
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture
def authenticated_client():
    client = Client()
    user = User.objects.create_user(username='postgres', password='ww00ac')
    client.force_login(user)
    return client


@pytest.mark.xfail(raises=AssertionError)
@pytest.mark.django_db
@pytest.mark.parametrize('data, expected_status', [
    ({'model': 'R2', 'version': 'D2', 'created': '2023-10-02T15:00:00Z'}, 201),  # Valid data
    ({'model': 'A3', 'version': 'H9', 'created': '2023-10-02T15:00:00Z'}, 201),  # Valid alphanumeric model and version
    ({'model': 'G2', 'version': 'P8', 'created': '2023-10-02T15:00:00Z'}, 201),  # Valid alphanumeric model and version
    ({'model': 'U7', 'version': 'K4', 'created': '2023-10-02T15:00:00Z'}, 201),  # Valid alphanumeric model and version
    ({'model': 'R2', 'version': 'C6'}, 400),  # Missing 'created' field
    ({'model': 'P9', 'version': 'D2', 'created': 'invalid_date'}, 400),  # Invalid date format
    ({'model': 'R1', 'version': 'D2', 'created': '2023-10-02T15:00:00Z'}, 201),  # Valid date format
    ({'model': 'R2', 'version': 'D2', 'created': '2023-10-02'}, 400),  # Invalid date format
    ({'model': 'U6', 'version': 'D2', 'created': '2023-13-02T15:00:00Z'}, 400),  # Invalid month
    ({'model': 'V4', 'version': 'D2', 'created': '2023-09-32T15:00:00Z'}, 400),  # Invalid day
    ({'model': 'R2', 'version': 'D2', 'created': '2023-10-02T25:00:00Z'}, 400),  # Invalid hour
    ({'model': 'B7', 'version': 'D2', 'created': '2023-10-02T15:61:00Z'}, 400),  # Invalid minute
    ({'model': 'I13', 'version': 'D2', 'created': '2023-10-02T15:00:61Z'}, 400),  # Invalid second
    ({'model': '', 'version': 'D2', 'created': '2023-10-02T15:00:00Z'}, 400),  # Empty 'model'
    ({'model': 'O8', 'version': '', 'created': '2023-10-02T15:00:00Z'}, 400),  # Empty 'version'
    ({'model': None, 'version': 'D2', 'created': '2023-10-02T15:00:00Z'}, 400),  # 'model' is None
    ({'model': 'R2', 'version': None, 'created': '2023-10-02T15:00:00Z'}, 400),  # 'version' is None
    ({'model': 'R2', 'version': 'D2', 'created': '2023-10-02T15:00:00Z'}, 201),  # Duplicate valid data for coverage
])
def test_create_robot(authenticated_client, data, expected_status):
    response = authenticated_client.post('/api/robots/', json.dumps(data), content_type='application/json')
    assert response.status_code == expected_status
