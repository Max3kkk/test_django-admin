from django.contrib import admin

from .models import Order


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        return (),

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class IdFilter(InputFilter):
    parameter_name = 'id'
    title = 'Id'

    def queryset(self, request, queryset):
        if self.value() is not None:
            obj_id = self.value()
            return queryset.filter(id=obj_id)


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
            return Order.objects.filter(_order_cost__lte=100)
        elif value == '<500':
            return Order.objects.filter(_order_cost__lte=500)
        elif value == '<1000':
            return Order.objects.filter(_order_cost__lte=1000)
        elif value == '<10000':
            return Order.objects.filter(_order_cost__lte=10000)
        return queryset
