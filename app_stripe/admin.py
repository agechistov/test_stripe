from django.contrib import admin

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
