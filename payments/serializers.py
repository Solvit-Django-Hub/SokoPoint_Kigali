from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    # Basic validation for payment amounts
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)

    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'transaction_id', 'payment_method', 'status', 'created_at']
        read_only_fields = ['transaction_id', 'status']

class CreatePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
    payment_method = serializers.CharField(required=True)
