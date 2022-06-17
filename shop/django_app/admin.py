from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponseRedirect

from .admin_filters import IdFilter, OrderSumFilter
from .models import Customer, Order, OrderItem, Product


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'phone_number', 'email')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'title', 'description',)
    list_filter = (IdFilter,)
    search_fields = ('title',)
    search_help_text = 'Input product title'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_select_related = ('customer',)
    actions = ['cancel_orders']
    inlines = [OrderItemInline, ]
    list_display = (
        'id', 'customer_name', 'customer_phone', 'customer_email', 'address', 'created_at', 'status', 'item_list',
        'order_cost')
    list_filter = ('status', 'customer__phone_number', 'created_at', OrderSumFilter)
    readonly_fields = (
        'id', 'status', 'customer_name', 'customer_phone', 'customer_email', 'created_at', 'order_cost')
    fields = (
        'id', 'customer', 'customer_name', 'customer_phone', 'customer_email', 'address', 'created_at', 'status',
        'order_cost')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _order_cost=Sum('item_prices__price'),
        )
        return queryset

    @admin.display(description='Cust. Name')
    def customer_name(self, obj):
        return obj.customer.name

    @admin.display(description='Cust. Phone Number')
    def customer_phone(self, obj):
        return obj.customer.phone_number

    @admin.display(description='Cust. Email')
    def customer_email(self, obj):
        return obj.customer.email

    @admin.display(description='Items')
    def item_list(self, obj):
        return list(OrderItem.objects.filter(order_id=obj.id))

    @admin.display(description='Total Cost')
    def order_cost(self, obj):
        return obj._order_cost

    change_form_template = "admin/cancel_order.html"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['is_cancelable'] = (Order.objects.get(
            pk=object_id).status != Order.Status.CANCELED) and "change" in request.path
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def response_change(self, request, obj):
        if "_cancel_order" in request.POST:
            obj.status = Order.Status.CANCELED
            obj.save()
            self.message_user(request, "This order has been canceled")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    @admin.action(description='Cancel Orders')
    def cancel_orders(self, request, queryset):
        queryset.update(status=Order.Status.CANCELED)


admin.site.register(OrderItem)
