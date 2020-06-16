import csv
import os
from orders.models import Salad
 
f = open("pizza.csv")
reader = csv.reader(f)
for dressing, price in reader:
  pizza = Salad(dressing=dressing, price=price)
  pizza.save()
  print(f"Added Pizza with {dressing}: small sells for {price}$ and large sells for {price}$.")
      



Salad.objects.all()



