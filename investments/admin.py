from django.contrib import admin

from .models import Asset, Portfolio, Price, Quantity, Weight

admin.site.register(Portfolio)
admin.site.register(Asset)
admin.site.register(Price)
admin.site.register(Weight)
admin.site.register(Quantity)
