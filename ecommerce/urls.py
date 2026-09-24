from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

def api_root(request):
    return JsonResponse({
        "status": "success",
        "message": "E-Commerce API is running!",
        "documentation": "/api/docs/"
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('users.urls')),
    path('api/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/', include('orders.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/', include('reviews.urls')),
    
    # Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
