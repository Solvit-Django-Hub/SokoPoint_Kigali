from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from products.models import Category, Product
from .models import Cart, CartItem

User = get_user_model()

class CartTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('user@example.com', 'UserPass123')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            description='A powerful laptop',
            price='999.99',
            stock_quantity=5,
            category=self.category
        )
        self.client.force_authenticate(user=self.user)

    def test_add_item_to_cart(self):
        """Ensure user can add item to cart."""
        data = {'product': self.product.id, 'quantity': 2}
        response = self.client.post('/api/cart/items/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.get().quantity, 2)

    def test_add_item_exceeds_stock(self):
        """Ensure stock validation works when adding."""
        data = {'product': self.product.id, 'quantity': 10}
        response = self.client.post('/api/cart/items/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('available in stock', response.data['message'] if 'message' in response.data else str(response.data))

    def test_view_cart_totals(self):
        """Ensure cart totals calculate correctly."""
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['data']['total_amount']), 1999.98)

    def test_clear_cart(self):
        """Ensure cart clearing works."""
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        response = self.client.delete('/api/cart/clear/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)
