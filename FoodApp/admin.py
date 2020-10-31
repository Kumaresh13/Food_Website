from django.contrib import admin
from .models import Item, OrderItem, Order
# Register your models here.
from import_export.admin import ImportExportModelAdmin


@admin.register(Item, OrderItem, Order)
class data(ImportExportModelAdmin):
    pass