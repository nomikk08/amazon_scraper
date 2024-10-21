from django.contrib import admin
from .models import Brand, Product

# Define inline admin for Product within Brand
class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

# Admin setup for the Brand model
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ProductInline]

# Admin setup for the Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'asin', 'sku', 'brand', 'image')
    search_fields = ('name', 'asin', 'sku', 'brand__name')
    list_filter = ('brand',)

