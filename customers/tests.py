import json
import pytest
from django.test import Client
from .models import Customer


@pytest.fixture
def create_customer():
    customer = Customer.objects.create(email="existingemail@example.com")
    return customer


@pytest.mark.django_db
@pytest.mark.parametrize("email, expected_status_code, expected_error_message", [
    ("validemail@example.com", 201, None),
    ("existingemail@example.com", 400, "Provided email already exists."),
    ("invalidemail", 400, """{"email": [{"message": "Enter a valid email address.", "code": "invalid"}]}"""),
    (None, 400, """{"email": [{"message": "This field is required.", "code": "required"}]}""")
])
def test_create_customer(create_customer, email, expected_status_code, expected_error_message):
    client = Client()
    data = {'email': email}
    response = client.post('/api/create_customer/', json.dumps(data), content_type='application/json')
    assert response.status_code == expected_status_code
    if expected_error_message:
        response_data = json.loads(response.content.decode('utf-8'))
        assert response_data['errors'] == expected_error_message
    else:
        customer = Customer.objects.filter(email=email).first()
        assert customer is not None
