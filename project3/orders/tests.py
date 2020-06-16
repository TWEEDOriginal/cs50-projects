from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from .models import *

user = User.objects.create_user("alice", "alice@something.com", "alice12345")
user.first_name = "Alice"

user.save()
user = authenticate(request, username="alice", password="alice12345")
login(request, user)
# Create your tests here.
class ModelsTestCase(TestCase):
        
    def setUp(self):


        # Create.
        Regular_pizza.objects.create(dressing="Ham + Cheese", small_price=6.50, large_price=7.50)
        Sicilian_pizza.objects.create(dressing="Ham + Cheese", small_price=6.50, large_price=7.50)
        Topping.objects.create(topping_name="Ham + Cheese")
        Dinner_platter.objects.create(dressing="Ham + Cheese", small_price=6.50, large_price=7.50) 
        Sub.objects.create(dressing="Ham + Cheese", small_price=6.50, large_price=7.50)
        Pasta.objects.create(dressing="Ham + Cheese", price=6.50)
        CartItem.create(dressing="Ham + Cheese", price=6.50)

    def test_topping_count(self):
        a = Regular_pizza.objects.get(dressing="Ham + Cheese")
        b = Topping.objects.get(topping_name="Ham + Cheese")
        a.toppings.add(b)

        self.assertEqual(a.toppings.count(), 1)


    def test_invalid_pizza(self):
        a = Sicilian_pizza.objects.get(dressing="Ham + Cheese")
        a.large_price = 6.50
       
        self.assertFalse(a.is_valid_pizza())
    
   