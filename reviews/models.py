from django.db import models
from django.conf import settings
from products.models import Product

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField() # Should validate 1-5 in serializers
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') # One review per user per product

    def __str__(self):
        return f"Review by {self.user.email} on {self.product.name}"
