from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import uuid
from .models import Payment
from orders.models import Order
from .serializers import PaymentSerializer, CreatePaymentSerializer

class PaymentView(views.APIView):
    """
    Demonstrates usage of simple APIView for processing payments.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']
        payment_method = serializer.validated_data['payment_method']

        # Ensure order exists and belongs to user
        order = get_object_or_404(Order, id=order_id, user=request.user)

        if order.status == 'cancelled':
            return Response({"message": "Cannot pay for a cancelled order."}, status=status.HTTP_400_BAD_REQUEST)
        if hasattr(order, 'payment') and order.payment.status == 'successful':
            return Response({"message": "Order is already paid."}, status=status.HTTP_400_BAD_REQUEST)

        # Mock payment processing
        transaction_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        
        payment, created = Payment.objects.get_or_create(order=order, defaults={
            'amount': order.total_amount,
            'payment_method': payment_method,
        })
        
        payment.transaction_id = transaction_id
        payment.status = 'successful'
        payment.save()

        # Update order status
        order.payment_status = 'paid'
        order.status = 'processing'
        order.save()

        response_serializer = PaymentSerializer(payment)
        return Response({
            "success": True,
            "message": "Payment processed successfully.",
            "data": response_serializer.data
        }, status=status.HTTP_201_CREATED)
