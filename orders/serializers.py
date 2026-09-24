from rest_framework import serializers
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_details', 'quantity', 'price', 'total_price']
        read_only_fields = ['price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'total_amount', 'shipping_address', 'phone_number', 'status', 'payment_status', 'created_at', 'items']
        read_only_fields = ['order_number', 'total_amount', 'status', 'payment_status']

class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
