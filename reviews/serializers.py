from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    
    # Rating validation 1-5
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_email', 'product', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'product']
