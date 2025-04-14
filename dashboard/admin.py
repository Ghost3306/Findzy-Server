from django.contrib import admin
from dashboard.models import StolenItem,StolenItemImage,Message,Notification,ReportItem


admin.site.register(StolenItem)
admin.site.register(StolenItemImage)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(ReportItem)
