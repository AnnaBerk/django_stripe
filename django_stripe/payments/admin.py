from django.contrib import admin

from .models import Item, Order, Discount, Tax


class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price']


admin.site.register(Item, ItemAdmin)
admin.site.register(Order)
admin.site.register(Discount)
admin.site.register(Tax)