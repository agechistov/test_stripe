from django.contrib import admin

from . import models as m


@admin.register(m.Item)
class ItemAdmin(admin.ModelAdmin):
    pass
