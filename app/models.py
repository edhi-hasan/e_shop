from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.

class Customer(models.Model):
    DIVISION_CHOICE = (
        ('Dhaka','Dhaka'),
        ('Chattogram','Chattogram'),
        ('Khulna','Khulna'),
        ('Rajshahi','Rajshahi'),
        ('Barishal','Barishal'),
        ('Rangpur','Rangpur'),
        ('Mymensingh ','Mymensingh '),
        ('Sylhet','Sylhet'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    division = models.CharField(choices=DIVISION_CHOICE, max_length=50)

    def __str__(self):
        return str(self.id)
    


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('M','Mobile'),
        ('L','Laptop'),
        ('TW','Top Wear'),
        ('BW','Bottom Wear'),
    )
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=5)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price

class OrderPlaced(models.Model):
    STATUS_CHOICE = (
        ('Accepted','Accepted'),
        ('Packed','Packed'),
        ('On The Way','On The Way'),
        ('Delivered','Delivered'),
        ('Cancel','Cancel'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICE,default='Pending')
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price