from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'order', 'amount', 'status', 'transaction_id', 'created_at']
    list_filter = ['status']
    search_fields = ['transaction_id', 'order__user__email', 'order__id']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    def get_user(self, obj):
        return obj.order.user.email
    get_user.short_description = 'User'
    