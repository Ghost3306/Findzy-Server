from django.contrib import admin
from dashboard.models import StolenItem,StolenItemImage


admin.site.register(StolenItem)
admin.site.register(StolenItemImage)