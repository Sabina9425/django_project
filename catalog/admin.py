from django.contrib import admin
from catalog.models import Category, Version
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


@admin.register(Version)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "version_name", "version_number", "product", "is_current_version")
    list_filter = ("product",)
    search_fields = ("product", "name",)
