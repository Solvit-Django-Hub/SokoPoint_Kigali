from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from products.models import Category, Product
from cart.models import Cart, CartItem
from .models import Order

User = get_user_model()

class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('user@example.com', 'UserPass123')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop', description='A laptop', price='999.99', stock_quantity=5, category=self.category
        )
        self.client.force_authenticate(user=self.user)

    def test_create_order(self):
        """Ensure order creation works and deducts stock."""
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        data = {
            'shipping_address': '123 Test St',
            'phone_number': '1234567890'
        }
        response = self.client.post('/api/orders/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().total_amount, 1999.98)
        
        # Verify stock deducted
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 3)
        
        # Verify cart cleared
        self.assertEqual(cart.items.count(), 0)
