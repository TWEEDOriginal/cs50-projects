from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import json
# Create your models here.
class Regular_pizza(models.Model):
      dressing = models.CharField(max_length=64)
      small_price = models.DecimalField(max_digits=5, decimal_places=2)
      large_price = models.DecimalField(max_digits=5, decimal_places=2)
      
      def clean(self):
         if self.small_price == self.large_price:
              raise ValidationError("You made a mistake in the pricing.")
         elif self.small_price < 1.00 or self.small_price < 1.00 :
              raise ValidationError("You made a mistake in the pricing.")
      def save(self, *args, **kwargs):
         self.clean()
         super().save(*args, **kwargs)

      def __str__(self):
           return f"{self.dressing} {self.small_price} {self.large_price}"

class Sicilian_pizza(models.Model):
      dressing = models.CharField(max_length=64)
      small_price = models.DecimalField(max_digits=5, decimal_places=2)
      large_price = models.DecimalField(max_digits=5, decimal_places=2)
      
      def is_valid_pizza(self):
        return (self.small_price != self.large_price)

      def __str__(self):
           return f"{self.dressing} {self.small_price} {self.large_price}"

class Topping(models.Model): 
      topping_name = models.CharField(max_length=64)
                 
      
      def __str__(self):
           return f"{self.topping_name}"   

class Sub(models.Model):
      dressing = models.CharField(max_length=64)
      small_price = models.DecimalField(max_digits=5, decimal_places=2)
      large_price = models.DecimalField(max_digits=5, decimal_places=2)

      def __str__(self):
           return f"{self.dressing} {self.small_price} {self.large_price}"           

class Pasta(models.Model):
      dressing = models.CharField(max_length=64)
      price = models.DecimalField(max_digits=5, decimal_places=2)

      def __str__(self):
           return f"{self.dressing} {self.price}"

class Salad(models.Model):
      dressing = models.CharField(max_length=64)
      price = models.DecimalField(max_digits=5, decimal_places=2)

      def __str__(self):
           return f"{self.dressing} {self.price}"           

class Dinner_platter(models.Model):
      dressing = models.CharField(max_length=64)
      small_price = models.DecimalField(max_digits=5, decimal_places=2)
      large_price = models.DecimalField(max_digits=5, decimal_places=2)

      def __str__(self):
           return f"{self.dressing} {self.small_price} {self.large_price}"


#class Cart(models.Model):           
    
     
   # def __str__(self):
    #     return f"{self.user} added this at {self.created_at}"            

class CartItem(models.Model):    
    created_at = models.DateTimeField(default=datetime.now)
    category = models.CharField(max_length=64, default= "pizza")
    dressing = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    toppings = models.ManyToManyField(Topping, blank=True, related_name="carts")
    created_by = models.CharField(max_length=64, default= "user_t")
   # cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")    

    def __str__(self):
        return f"{self.created_by} {self.category} ({self.dressing} with price {self.price})"


class OrderItem(models.Model):
      user = models.CharField(max_length=64)
      token = models.CharField(max_length=120, default = "fuck")
      category = models.CharField(max_length=64)
      dressing = models.CharField(max_length=64)
      topping = models.CharField(max_length=200, default = "none")
      def set_topping(self,x):
        self.topping = json.dumps(x)
      def get_topping(self):
         return json.loads(self.topping)  
      price = models.DecimalField(max_digits=5, decimal_places=2)
      time_of_order = models.DateTimeField(default=datetime.now)

      def __str__(self):
        return f"{self.user} {self.token} {self.category} ({self.dressing} with price {self.price}) and toppings:{self.topping} ordered at the time {self.time_of_order}" 