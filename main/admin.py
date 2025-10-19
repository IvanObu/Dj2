from django.contrib import admin

from .models import Category, Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug', 'price', 'created', 'uploaded', 'discount', 'available']
    list_filter = ['available', 'created', 'uploaded']
    list_editable = ['price', 'available', 'discount']
    search_fields = ['name', 'price', 'description']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}



