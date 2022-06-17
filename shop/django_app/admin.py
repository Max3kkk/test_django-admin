from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponseRedirect

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
    list_filter = ('id',)
    search_fields = ('title',)


class OrderSumFilter(admin.SimpleListFilter):
    title = 'Order Total sum'
    parameter_name = 'order_total_cost'

    def lookups(self, request, model_admin):
        return (
            ('<100', 'less than 100rub'),
            ('<500', 'less than 500rub'),
            ('<1000', 'less than 10000rub'),
            ('<10000', 'less than 10000rub'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == '<100':
            return Order.objects.annotate(total_cost=Sum('item_prices__price')).filter(total_cost__lte=100)
        elif value == '<500':
            return Order.objects.annotate(total_cost=Sum('item_prices__price')).filter(total_cost__lte=500)
        elif value == '<1000':
            return Order.objects.annotate(total_cost=Sum('item_prices__price')).filter(total_cost__lte=1000)
        elif value == '<10000':
            return Order.objects.annotate(total_cost=Sum('item_prices__price')).filter(total_cost__lte=10000)
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
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
        return list(OrderItem.objects.filter(order=obj.id))

    @admin.display(description='Total Cost')
    def order_cost(self, obj):
        return sum(list(OrderItem.objects.filter(order=obj.id).values_list('price', flat=True)))

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
