from django.contrib import admin
from .models import Account, AccountType, Order


class AInline(admin.TabularInline):
    model = Account
    extra = 0


class AccountTypeAdmin(admin.ModelAdmin):
    inlines = [AInline]

    class Meta:
        model = AccountType


class AccountAdmin(admin.ModelAdmin):
    list_display = ['type', 'order', 'login', 'is_active']
    search_fields = ['type', 'order']
    list_filter = ['type', 'order']

    class Meta:
        model = Account


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'count', 'created', 'total_price', 'paid', 'complete']
    list_filter = ['paid']


admin.site.register(Account, AccountAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Order, OrderAdmin)
