from django.db import models

# Create your models here.

class ProductType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, default='')
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, default='')
    price = models.IntegerField(default=0)
    ProductType = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    total_price = models.IntegerField(default=0)
    products = models.ManyToManyField(Product, through='Order_Product')

class Order_Product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)