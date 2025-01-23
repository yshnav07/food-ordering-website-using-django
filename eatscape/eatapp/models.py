from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Userprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.TextField()
    pincode=models.TextField()
    address=models.CharField(max_length=255)

class details_new(models.Model):
    restaurantName=models.TextField()
    address=models.CharField(max_length=255)
    pincode=models.TextField()
    location=models.TextField()
    longitude=models.TextField()
    latitude=models.TextField()
    cuisine=models.TextField()
    is_active= models.BooleanField(default=True)
    contact = models.CharField(max_length=15) 
    image = models.ImageField(upload_to='rest_images',null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class menu_new(models.Model):
    restaurant = models.ForeignKey(details_new, on_delete=models.CASCADE, related_name='menu')
    menuItemName=models.TextField()
    description=models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category=models.TextField()
    carted = models.BooleanField(default=False)
    availability=models.TextField()
    image1= models.ImageField(upload_to='menu_images',null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active= models.BooleanField(default=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active= models.BooleanField(default=True)

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(menu_new, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active= models.BooleanField(default=True)

class payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    paymentOption=models.TextField()
    cardNumber=models.IntegerField()
    cardholderName=models.TextField()
    


    def __str__(self):
        return self.user.username.__str__()
