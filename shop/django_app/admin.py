from django.contrib import admin
from .models import Customer, Order, OrderItem, Product


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'email')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description',)
    list_filter = ('id',)
    search_fields = ('title',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cust_name', 'get_cust_phone', 'get_cust_email', 'address', 'status')
    list_filter = ('status', 'customer_id__phone_number')

    def get_cust_name(self, obj):
        return obj.customer_id.name
    get_cust_name.short_description = 'Customer Name'
    get_cust_name.admin_order_name = 'customer_id__name'

    def get_cust_phone(self, obj):
        return obj.customer_id.phone_number
    get_cust_phone.short_description = 'Customer Phone Number'
    get_cust_name.admin_order_name = 'customer_id__phone_number'

    def get_cust_email(self, obj):
        return obj.customer_id.email
    get_cust_email.short_description = 'Customer Email'
    get_cust_name.admin_order_name = 'customer_id__email'


admin.site.register(OrderItem)
