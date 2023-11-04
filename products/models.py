from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"
    

class Color(models.Model):
    name = models.CharField(max_length=255)
    color_code = ColorField(default='#FF0000')

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")
        ordering = ("name",)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    background_color  = models.ForeignKey('products.Color', on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"
    


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to='upload/Category',blank=True,null=True)

    
    class Meta:
        ordering = ['id',]
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')


    def get_subcategories(self):
        return SubCategory.objects.filter(category=self)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to='upload/SubCategory',blank=True,null=True)
    is_popular = models.BooleanField(default=True)

    class Meta:
        ordering = ['id',]
        verbose_name = ('SubCategory')
        verbose_name_plural = ('SubCategories')

    def get_product_count(self):
        return self.subcategory.count()
    
    def get_products(self):
        return Product.objects.filter(subcategory=self)
    
    def __str__(self):
        return f"{self.category} - {self.title}"


class ProductSize(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255,unique=True)

    class Meta:
        verbose_name = _("Product Size")
        verbose_name_plural = _("Product Sizes")
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"   
    

class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name='subcategory')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,blank=True,null=True)
    tag = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField()
    vendor = models.CharField(max_length=100,blank=True,null=True)
    sku = models.SlugField(max_length=100,blank=True,null=True,unique=True)
    image = models.ImageField(upload_to='upload/products')
    rating=models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],default=5,verbose_name="Product Rating(max:5)"
    )
    is_new_arrival = models.BooleanField(default=True)
    is_best_seller = models.BooleanField(default=True)
    is_top_rated = models.BooleanField(default=True)

    class Meta:
        ordering = ['id',]
        verbose_name = ('Product')
        verbose_name_plural = ('Products')

    
    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Product, self).delete(*args, **kwargs)
        storage.delete(path)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def get_images(self):
        return ProductImage.objects.filter(product=self)

    def get_additional(self):
        return ProductAdditional.objects.filter(product=self).first()
    
    def get_features(self):
        return ProductFeature.objects.filter(product=self)

    def get_colors(self):
         return ProductImage.objects.filter(product=self).distinct()

    def get_sizes(self):
        return AvailableSize.objects.filter(product=self)

    def get_sale_price(self):
        return min([p.sale_price for p in self.get_sizes()])

    def get_original_price(self):
        sizes = self.get_sizes()
        valid_prices = [p.original_price for p in sizes if p.original_price is not None]
        return min(valid_prices) if valid_prices else None

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.slug})

    def related_products(self):
        return Product.objects.filter().exclude(pk=self.pk).distinct()[0:12]


    def __str__(self):
        return f"{self.brand}: {self.title}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    color = models.ForeignKey('products.Color', on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ("product",)

    def __str__(self):
        return str(self.name)
    

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    point = models.TextField(max_length=500)

    class Meta:
        verbose_name = _("Product Feature")
        verbose_name_plural = _("Product Features")
        ordering = ("point",)

    def __str__(self):
        return f"{self.point}"


class ProductAdditional(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=150,blank=True,null=True)
    dimension = models.CharField(max_length=150,blank=True,null=True)
    first_available =models.DateField(blank=True,null=True)
    
    class Meta:
        verbose_name = _("Product Additional")
        verbose_name_plural = _("Product Additionals")
        ordering = ("id",)

    def __str__(self):
        return f"{self.manufacturer}"
    

class AvailableSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey('products.ProductSize', on_delete=models.CASCADE)
    color = models.ForeignKey('products.Color', on_delete=models.CASCADE,blank=True,null=True)
    sale_price = models.FloatField()
    original_price = models.FloatField(blank=True, null=True)
    opening_stock = models.IntegerField()
    minimum_order_qty = models.IntegerField(default=1)


    class Meta:
        verbose_name = _("Available Size")
        verbose_name_plural = _("Available Sizes")
        ordering = ("sale_price",)


    def __str__(self):
        return f"{self.color} / {self.size.code} - {self.sale_price}"

    def save(self, *args, **kwargs):
        if self.original_price is None:
            self.original_price = self.sale_price
        super().save(*args, **kwargs)
    
