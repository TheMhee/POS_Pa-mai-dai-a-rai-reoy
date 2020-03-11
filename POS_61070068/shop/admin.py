from shop.models import Product,ProductType
from django.contrib.auth.models import Permission, User
from django.contrib import admin

# Register your models here.
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_per_page = 10
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(ProductType, TypeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'ProductType', 'description', 'price']
    list_per_page = 10
    list_filter = ['name', 'price']
    search_fields = ['name']

admin.site.register(Product, ProductAdmin)
admin.site.register(Permission)