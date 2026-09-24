from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Review
from .serializers import ReviewSerializer
from products.models import Product

class ReviewListCreateView(generics.ListCreateAPIView):
    """
    Demonstrates Generic Views. 
    Lists reviews for a product or creates a new one.
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product_id=product_id).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        # Check if user already reviewed
        if Review.objects.filter(user=request.user, product=product).exists():
            return Response({"message": "You have already reviewed this product."}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Demonstrates RetrieveUpdateDestroyAPIView for single review management.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user and self.request.user.role != 'admin':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only edit your own reviews.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user and self.request.user.role != 'admin':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own reviews.")
        instance.delete()
