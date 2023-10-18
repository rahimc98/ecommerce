from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['id',]
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    
    class Meta:
        ordering = ['id',]
        verbose_name = ('SubCategory')
        verbose_name_plural = ('SubCategories')

    
    def __str__(self):
        return f"{self.category} - {self.title}"
    
    def get_product_count(self):
        return self.subcategory.count()
        

class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name='subcategory')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='upload/products')

    class Meta:
        ordering = ['id',]
        verbose_name = ('Product')
        verbose_name_plural = ('Products')

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Product, self).delete(*args, **kwargs)
        storage.delete(path)
