from django.contrib import admin
from catalog.models import Category
from catalog.models import Product, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "header", "views", "published")
    list_filter = ("header",)
    search_fields = ("header", "content",)
