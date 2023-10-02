from django.contrib import admin
from products.models import Category, SubCategory, Product
from django.contrib.auth.models import User, Group

# To remove user,groups from admin panel
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", )
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("title", )
    
    search_fields = (
        "title",
    )


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("title",'category' )
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("title",'category' )
    # autocomplete_fields = ("category",)
    search_fields = (
        "title",
        'category__title',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title",'subcategory','price' )
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("title",'subcategory' )
    autocomplete_fields = ("subcategory",)
    search_fields = (
        "title",
        'subcategory__title',
    )
