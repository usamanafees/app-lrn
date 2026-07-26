import pytest
from rest_framework.test import APIClient
from customers.models import Customer
from billing.models import LineItem
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_list_line_items():
    client = APIClient()
    
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)

    customer = Customer.objects.create(name='Test Co', email='test@example.com')
    LineItem.objects.create(customer=customer, kwh='10.00', rate='0.1200')

    response = client.get('/api/line-items/')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['kwh'] == '10.00'

@pytest.mark.django_db
def test_create_line_item_rejects_negative_kwh():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)
    
    customer = Customer.objects.create(name='Test Co', email='test@example.com')

    response = client.post('/api/line-items/', {
        'customer': customer.id,
        'kwh': '-5.00',
        'rate': '0.1200',
    }, format='json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_total_by_customer():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)

    customer = Customer.objects.create(name='Test Co', email='test@example.com')
    LineItem.objects.create(customer=customer, kwh='10.00', rate='0.1200')

    response = client.get(f'/api/line-items/total-by-customer/?customer_id={customer.id}')

    assert response.status_code == 200
    assert response.data['total'] == '1.20'



@pytest.mark.django_db
def test_unauthenticated_get_returns_401():
    client = APIClient()
    response = client.get('/api/line-items/total-by-customer/?customer_id=1')
    assert response.status_code == 403

@pytest.mark.django_db
def test_list_is_public_without_auth():
    client = APIClient()
    response = client.get('/api/line-items/')
    assert response.status_code == 200

#     Fixed vs yours — line by line
# Code	Fixed/yours	Meaning
# @pytest.mark.django_db
# Fixed
# allows test to use DB
# APIClient
# Fixed DRF
# fake HTTP client
# client.get('/api/line-items/')
# Fixed .get
# HTTP GET — URL yours
# response.status_code
# Fixed
# 200, 400, 404, etc.
# response.data
# Fixed DRF
# parsed JSON
# assert
# Fixed Python
# test pass/fail
# test_list_line_items
# Yours
# test function name