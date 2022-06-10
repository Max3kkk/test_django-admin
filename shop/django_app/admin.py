from django.contrib import admin
from .models import Customer, Order, OrderItem, Product


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'email')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', )
    list_filter = ('id', )
    search_fields = ('title', )


admin.site.register(Order)
admin.site.register(OrderItem)
