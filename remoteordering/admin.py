from django.contrib import admin
from .models import Menu_item,Order,Order_management,Restaurant_details

# Register your models here.
admin.site.register(Menu_item)
admin.site.register(Order)
admin.site.register(Order_management)
admin.site.register(Restaurant_details)
