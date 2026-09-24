from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Category, Product

User = get_user_model()

class ProductTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin@example.com', 'AdminPass123')
        self.regular_user = User.objects.create_user('user@example.com', 'UserPass123')
        
        self.category = Category.objects.create(name='Electronics')
        self.product_data = {
            'name': 'Laptop',
            'description': 'A powerful laptop',
            'price': '999.99',
            'stock_quantity': 10,
            'category': self.category.id
        }

    def test_create_product_as_admin(self):
        """Ensure admin can create product."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post('/api/products/', self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_create_product_as_regular_user_fails(self):
        """Ensure regular user cannot create product."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post('/api/products/', self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_products_public(self):
        """Ensure anyone can view products."""
        Product.objects.create(name='Laptop', description='A laptop', price='999.99', category=self.category)
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_product_search(self):
        """Ensure product searching works."""
        Product.objects.create(name='Laptop', description='A laptop', price='999.99', category=self.category)
        Product.objects.create(name='Mouse', description='A mouse', price='29.99', category=self.category)
        
        response = self.client.get('/api/products/?search=Laptop')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Laptop')
