from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import Customer, Order, OrderItem, Product


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'phone_number', 'email')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product_id', 'quantity', 'price',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'title', 'description',)
    list_filter = ('id',)
    search_fields = ('title',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = ['cancel_orders']
    inlines = [OrderItemInline, ]
    list_display = (
        'id', 'get_cust_name', 'get_cust_phone', 'get_cust_email', 'address', 'created_at', 'status', 'get_items',
        'calc_order_sum')
    list_filter = ('status', 'customer_id__phone_number', 'created_at')
    readonly_fields = (
        'id', 'status', 'get_cust_name', 'get_cust_phone', 'get_cust_email', 'created_at', 'calc_order_sum')
    fields = (
        'id', 'customer_id', 'get_cust_name', 'get_cust_phone', 'get_cust_email', 'address', 'created_at', 'status',
        'calc_order_sum')

    def get_cust_name(self, obj):
        return obj.customer_id.name

    get_cust_name.short_description = 'Cust. Name'
    get_cust_name.admin_order_name = 'customer_id__name'

    def get_cust_phone(self, obj):
        return obj.customer_id.phone_number

    get_cust_phone.short_description = 'Cust. Phone Number'
    get_cust_name.admin_order_name = 'customer_id__phone_number'

    def get_cust_email(self, obj):
        return obj.customer_id.email

    get_cust_email.short_description = 'Cust. Email'
    get_cust_name.admin_order_name = 'customer_id__email'

    def get_items(self, obj):
        return list(OrderItem.objects.filter(order_id=obj.id))

    get_items.short_description = 'Items'

    def calc_order_sum(self, obj):
        return sum(list(OrderItem.objects.filter(order_id=obj.id).values_list('price', flat=True)))

    calc_order_sum.short_description = 'Sum'

    change_form_template = "admin/cancel_order.html"

    def response_change(self, request, obj):
        if "_cancel_order" in request.POST:
            obj.status = 'Canceled'
            obj.save()
            self.message_user(request, "This order has been canceled")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    @admin.action(description='Cancel Orders')
    def cancel_orders(self, request, queryset):
        queryset.update(status='Canceled')


admin.site.register(OrderItem)
