from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
import uuid
from .models import Order, OrderItem
from cart.models import Cart
from .serializers import OrderSerializer, CreateOrderSerializer

class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Demonstrates usage of Mixins and GenericViewSet.
    Handles listing, retrieving, and creating orders.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cart = Cart.objects.get(user=request.user)
            if not cart.items.exists():
                return Response({"message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Create Order
            order = Order.objects.create(
                user=request.user,
                order_number=str(uuid.uuid4().hex[:10]).upper(),
                shipping_address=serializer.validated_data['shipping_address'],
                phone_number=serializer.validated_data['phone_number'],
                total_amount=0
            )

            total_amount = 0
            for cart_item in cart.items.all():
                # Business Rule Validation: Check stock before creating order
                if cart_item.quantity > cart_item.product.stock_quantity:
                    raise ValueError(f"Insufficient stock for {cart_item.product.name}")

                # Deduct stock
                cart_item.product.stock_quantity -= cart_item.quantity
                cart_item.product.save()

                # Create Order Item (store historical price)
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                total_amount += (cart_item.product.price * cart_item.quantity)

            order.total_amount = total_amount
            order.save()

            # Clear Cart after successful order
            cart.items.all().delete()

        response_serializer = OrderSerializer(order)
        return Response({
            "success": True,
            "message": "Order created successfully",
            "data": response_serializer.data
        }, status=status.HTTP_201_CREATED)
