from django.db import models
# from app.models import User
# Create your models here.
import requests

class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return f'{self.name} - {self.price} | {self.category}'
    
            
class Size(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name_plural = 'Sizes'
    def __str__(self):
        return self.name

    
class Color(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
            verbose_name_plural = 'Colors'
    def __str__(self):
        return self.name


class ProductSizeNColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            verbose_name_plural = 'ProductSizeNColors'
    
    def __str__(self):
        return f'{self.product} - {self.size} | {self.color} | {self.stock_quantity}'


    
class SubProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()
    # image = models.ImageField(upload_to='images/products/')
    image = models.CharField(max_length=5000, null=True, blank=True, default='')
    product_size_color = models.ManyToManyField(ProductSizeNColor)
    # color = models.CharField(max_length=50)
    # quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # sizes = models.ManyToManyField(Size, through='SizeSubProduct')

    def get_stock_quantity(self):
        return sum([psc.stock_quantity for psc in self.product_size_color.all()])
    
    class Meta:
            verbose_name_plural = 'SubProducts'
    def __str__(self):
        return f'{self.product}'
    
