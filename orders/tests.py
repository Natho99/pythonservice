from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Customer, Order

class CustomerOrderAPITests(APITestCase):

    def setUp(self):
        # Set up the test user and log them in
        self.user = User.objects.create_user(username='nathan', password='Nathoo@99')
        self.client = APIClient()

        # Check if login is successful
        login_successful = self.client.login(username='nathan', password='Nathoo@99')
        assert login_successful, "Test user login failed"

        # Create a sample customer with phone number
        self.customer_data = {
            'name': 'Test Customer',
            'code': 'C001',
            'phone_number': '1234567890'  # New phone number field
        }
        self.customer = Customer.objects.create(**self.customer_data)

        # Data for an order
        self.order_data = {
            'customer': self.customer.id,
            'item': 'Test Item',
            'amount': '100.00'
        }

    def test_create_customer(self):
        response = self.client.post('/api/customers/', self.customer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Customer')
        self.assertEqual(response.data['code'], 'C001')
        self.assertEqual(response.data['phone_number'], '254700423736')  # Assert phone number

    def test_get_customers(self):
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Customer')
        self.assertEqual(response.data[0]['phone_number'], '254700423736')  # Assert phone number

    def test_get_single_customer(self):
        response = self.client.get(f'/api/customers/{self.customer.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Customer')
        self.assertEqual(response.data['phone_number'], '254700423736')  # Assert phone number

    def test_create_order(self):
        response = self.client.post('/api/orders/', self.order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['item'], 'Test Item')
        self.assertEqual(response.data['amount'], '100.00')

    def test_get_orders(self):
        # Create an order before retrieving orders
        self.client.post('/api/orders/', self.order_data)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['item'], 'Test Item')

    def test_get_single_order(self):
        # Create an order before retrieving the specific order
        response = self.client.post('/api/orders/', self.order_data)
        order_id = response.data['id']

        response = self.client.get(f'/api/orders/{order_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['item'], 'Test Item')

    def test_create_order_missing_customer(self):
        invalid_order_data = {
            'item': 'Test Item',
            'amount': '100.00'
        }
        response = self.client.post('/api/orders/', invalid_order_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_customer(self):
        response = self.client.delete(f'/api/customers/{self.customer.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)

    def test_delete_order(self):
        # Create an order first
        response = self.client.post('/api/orders/', self.order_data)
        order_id = response.data['id']

        response = self.client.delete(f'/api/orders/{order_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
