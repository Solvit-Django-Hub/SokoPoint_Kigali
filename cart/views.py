from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

class CartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response({
            "success": True,
            "message": "Cart retrieved successfully",
            "data": serializer.data
        })

    def delete(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        return Response({
            "success": True,
            "message": "Cart cleared successfully",
            "data": {}
        }, status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def create(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({"success": False, "message": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(Product, id=product_id)

        if not product.active:
            return Response({"success": False, "message": "Product is inactive"}, status=status.HTTP_400_BAD_REQUEST)

        # Check stock
        if quantity > product.stock_quantity:
            return Response({"success": False, "message": f"Only {product.stock_quantity} items available in stock."}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            if cart_item.quantity + quantity > product.stock_quantity:
                return Response({"success": False, "message": f"Exceeds stock. Only {product.stock_quantity} available."}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
            
        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response({
            "success": True,
            "message": "Item added to cart",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        quantity = request.data.get('quantity')

        if quantity is not None:
            if int(quantity) > instance.product.stock_quantity:
                return Response({"success": False, "message": f"Exceeds stock. Only {instance.product.stock_quantity} available."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            "success": True,
            "message": "Cart item updated",
            "data": serializer.data
        })
