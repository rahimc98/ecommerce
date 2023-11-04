from django.contrib import admin
from products.models import Category, SubCategory, Product,ProductFeature,ProductAdditional
from django.contrib.auth.models import User, Group
from .models import AvailableSize,Tag
from .models import Brand,Color
from .models import ProductImage
from .models import ProductSize
from django.utils.safestring import mark_safe

# To remove user,groups from admin panel
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",'image_preview' )
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("title", )
    
    search_fields = (
        "title",
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = 'Image Preview'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("title",'category','image_preview' )
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("title",'category' )
    # autocomplete_fields = ("category",)
    search_fields = (
        "title",
        'category__title',
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = 'Image Preview'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 0

class AvailableSizeInline(admin.TabularInline):
    model = AvailableSize
    extra = 0
    autocomplete_fields = ('size',)


class ProductAdditionalInline(admin.TabularInline):
    model = ProductAdditional
    extra = 0
    max_num =1

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug','background_color')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title",'subcategory','image_preview' )
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('subcategory', 'subcategory__category')
    autocomplete_fields = ("subcategory",)
    inlines = [ProductAdditionalInline,ProductFeatureInline,ProductImageInline,AvailableSizeInline]
    search_fields = (
        "title",
        'subcategory__title',
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = 'Image Preview'


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name',)


@admin.register(AvailableSize)
class AvailableSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size')
    search_fields = ('product__name',)
    autocomplete_fields = ('product', 'size')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name','color_code')