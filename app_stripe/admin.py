from django.contrib import admin
from django.forms import BaseInlineFormSet, ValidationError

from . import models as m


@admin.register(m.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_select_related = ["currency"]


@admin.register(m.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "price",
        "currency",
    ]


class OrderItemInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        currencies = {
            f.cleaned_data["item"].currency
            for f in self.forms
            if f.cleaned_data and not f.cleaned_data.get("DELETE")
        }
        if len(currencies) > 1:
            raise ValidationError(
                "В заказе можно указать только item-ы одинаковой валюты."
            )

        items = [
            f.cleaned_data["item"].id
            for f in self.forms
            if f.cleaned_data and not f.cleaned_data.get("DELETE")
        ]
        if len(items) != len(set(items)):
            raise ValidationError("По-идее гуд, когда каждый item в заказе уникален.")


class OrderItemInline(admin.StackedInline):
    model = m.OrderItem
    extra = 1
    formset = OrderItemInlineFormSet


@admin.register(m.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
