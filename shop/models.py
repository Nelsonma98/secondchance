from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    contact_phone = models.CharField()
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Ad(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField()
    image = models.ImageField(upload_to='ads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name