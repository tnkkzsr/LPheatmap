from django.contrib import admin
from .models import AttentionData,ClickData,ScrollData
# Register your models here.
admin.site.register(AttentionData)
admin.site.register(ClickData)
admin.site.register(ScrollData)