from django.contrib import admin
from .models import Asset, Price, Weight, Portfolio

admin.site.register(Portfolio)
admin.site.register(Asset)
admin.site.register(Price)
admin.site.register(Weight)

