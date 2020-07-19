from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
import os, json 
import requests
import stripe

# This is your real test secret API key.

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    context = {
        "user": request.user,
        "Regular_pizzas": Regular_pizza.objects.all(),
        "Sicilian_pizzas": Sicilian_pizza.objects.all(),
        "Toppings": Topping.objects.all(),
        "Subs": Sub.objects.all(),
        "Pastas": Pasta.objects.all(),
        "Salads": Salad.objects.all(),
        "Dinner_platters": Dinner_platter.objects.all()
    }
    return render(request, "orders/user.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})

def signup_view(request):
   if request.method == 'POST':
       username = request.POST["username"]
       raw_password = request.POST["password"]
       e_mail = request.POST["e_mail"]
       
       if username.strip() == "" or raw_password.strip() == "" or e_mail.strip() == "" :
             return render(request, "orders/signup.html", {"message": "Invalid credentials."})
       first_name = username.capitalize()
       user = User.objects.create_user(username, e_mail, raw_password)
       user.first_name = first_name
       user.save()
       
       return render(request,"orders/success.html")
       
   else:
       return render(request, "orders/signup.html", {"message": None})     


def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})


def add_r_s_to_cart(request):    
    try:
        r_s_price = float(request.POST["r_s_price"])
        firstname = request.user.first_name
        food = Regular_pizza.objects.get(small_price=r_s_price)
    except KeyError:    
        return render(request, "orders/error.html", {"message": "No selection."})
    except Regular_pizza.DoesNotExist:    
        return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."})
    #if pizza.id != food.id :    
     #   return render(request, "orders/error.html", {"message": "there is an error I do not comprehend, fuck 12."})
    f = CartItem(category = "Regular Pizza", dressing=food.dressing, price=food.small_price, created_by = firstname) 
    f.save()   
    return HttpResponseRedirect(reverse("index"))


def add_r_l_to_cart(request):    
    try:
        r_l_price = float(request.POST["r_l_price"])
        firstname = request.user.first_name
        #pizza = Regular_pizza.objects.get(pk=r_l_pizza_id)
        food = Regular_pizza.objects.get(large_price=r_l_price)
    except KeyError:    
        return render(request, "orders/error.html", {"message": "No selection."})
    except Regular_pizza.DoesNotExist:    
        return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."})
    #if pizza.id != food.id :    
     #   return render(request, "orders/error.html", {"message": "there is an error I do not comprehend, fuck 12."})
    f = CartItem(category = "Regular Pizza",dressing=food.dressing, price=food.large_price, created_by = firstname) 
    f.save()   
    return HttpResponseRedirect(reverse("index"))    


def add_s_s_to_cart(request):    
    try:
        s_s_price = float(request.POST["s_s_price"])
        firstname = request.user.first_name
       # pizza = Sicilian_pizza.objects.get(pk=s_s_pizza_id)
        food = Sicilian_pizza.objects.get(small_price=s_s_price)

    except KeyError:    
        return render(request, "orders/error.html", {"message": "No selection."})
    except Sicilian_pizza.DoesNotExist:    
        return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."})
  #  if pizza.id != food.id :    
  #      return render(request, "orders/error.html", {"message": "there is an error I do not comprehend, fuck 12."})
    f = CartItem(category = "Sicilian Pizza", dressing=food.dressing, price=food.small_price, created_by = firstname) 
    f.save()   
    return HttpResponseRedirect(reverse("index")) 


def add_s_l_to_cart(request):    
    try:
        s_l_price = float(request.POST["s_l_price"])
        firstname = request.user.first_name
        food = Sicilian_pizza.objects.get(large_price=s_l_price)
    except KeyError:    
        return render(request, "orders/error.html", {"message": "No selection."})
    except Sicilian_pizza.DoesNotExist:    
        return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."})
   # if pizza.id != food.id :    
   #     return render(request, "orders/error.html", {"message": "there is an error I do not comprehend, fuck 12."})
    f = CartItem(category = "Sicilian Pizza", dressing=food.dressing, price=food.large_price, created_by = firstname) 
    f.save()   
    return HttpResponseRedirect(reverse("index"))         



def add_Sub_s_to_cart(request):    
    try:
        Sub_s_price = int(request.POST["Sub_s_price"])
        firstname = request.user.first_name
        food = Sub.objects.get(pk=Sub_s_price)
    except KeyError:    
        return render(request, "orders/error.html", {"message": "No selection."})
    except Sub.DoesNotExist:    
        return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."})
   # if pizza.id != food.id :    
    #    return render(request, "orders/error.html", {"message": "there is an error I do not comprehend, fuck 12."})
    f = CartItem(category = "Sub", dressing=food.dressing, price=food.small_price, created_by = firstname) 
    f.save()   
    return HttpResponseRedirect(reverse("index")) 


def add_Sub_l_to_cart(request):    
    try:
        Sub_l_price = int(request.POST["Sub_l_price"])
        firstname = request.user.first_name
        food = Sub.objects.get(pk=Sub_l_price)
    except KeyError:    
        return render(request, "orders/error.html", {"message": "No selection."})
    except Sub.DoesNotExist:    
        return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."})
   # if pizza.id != food.id :    
    #    return render(request, "orders/error.html", {"message": "there is an error I do not comprehend, fuck 12."})
    f = CartItem(category = "Sub", dressing=food.dressing, price=food.large_price, created_by = firstname) 
    f.save()   
    return HttpResponseRedirect(reverse("index")) 


def add_p_to_cart(request):    
    try:
        p_price = float(request.POST["p_price"])
        firstname = request.user.first_name
        food = Pasta.objects.get(price=p_price)
    except KeyError:    
        return render(request, "orders/error.html", {"message": "No selection."})
    except Pasta.DoesNotExist:    
        return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."})
 #   if pizza.id != food.id :    
   #     return render(request, "orders/error.html", {"message": "there is an error I do not comprehend, fuck 12."})
    f = CartItem(category = "Pasta", dressing=food.dressing, price=food.price, created_by = firstname) 
    f.save()   
    return HttpResponseRedirect(reverse("index")) 


def add_salad_to_cart(request):    
    try:
        salad_price = int(request.POST["salad_price"])
        firstname = request.user.first_name
        food = Salad.objects.get(pk=salad_price)
    except KeyError:    
        return render(request, "orders/error.html", {"message": "No selection."})
    except Salad.DoesNotExist:    
        return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."})
  #  if pizza.id != food.id :    
 #       return render(request, "orders/error.html", {"message": "there is an error I do not comprehend, fuck 12."})
    f = CartItem(category = "Salad", dressing=food.dressing, price=food.price, created_by = firstname) 
    f.save()   
    return HttpResponseRedirect(reverse("index")) 



def add_d_s_to_cart(request):    
    try:
        d_s_price = int(request.POST["d_s_price"])
        firstname = request.user.first_name
        food = Dinner_platter.objects.get(pk=d_s_price)
    except KeyError:    
        return render(request, "orders/error.html", {"message": "No selection."})
    except Dinner_platter.DoesNotExist:    
        return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."})
  #  if pizza.id != food.id :    
   #     return render(request, "orders/error.html", {"message": "there is an error I do not comprehend, fuck 12."})
    f = CartItem(category = "Dinner Platter", dressing=food.dressing, price=food.small_price, created_by = firstname) 
    f.save()   
    return HttpResponseRedirect(reverse("index")) 


def add_d_l_to_cart(request):    
    try:
        d_l_price = int(request.POST["d_l_price"])
        firstname = request.user.first_name
        food = Dinner_platter.objects.get(pk=d_l_price)
    except KeyError:    
        return render(request, "orders/error.html", {"message": "No selection."})
    except Dinner_platter.DoesNotExist:    
        return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."})
  #  if pizza.id != food.id :    
    #    return render(request, "orders/error.html", {"message": "there is an error I do not comprehend, fuck 12."})
    f = CartItem(category = "Dinner Platter", dressing=food.dressing, price=food.large_price, created_by = firstname) 
    f.save()   
    return HttpResponseRedirect(reverse("index"))  

def cart(request):
     firstname = request.user.first_name
     a =  CartItem.objects.filter(created_by = firstname)
         
     if a.count() == 0:
        return render(request, "orders/error.html", {"message": "Your Cart is empty."})
     x = 0
     for i in a:
         x += i.price     
     context = {
        "CartItems": a,
        "Toppings": Topping.objects.all(),
        "Total": x
     }   
     return render(request, "orders/cart.html", context)


def add_topping(request):
    firstname = request.user.first_name
    b =  CartItem.objects.filter(created_by = firstname)
    a = CartItem.objects.filter(category = "Regular Pizza")
    
    if a.count == 0 or b.count == 0:
       return render(request, "orders/error.html", {"message": "Your Cart does not have a Regular pizza."})    
        
    context = {
    "CartItems": b,
    "Toppings": Topping.objects.all()
    }
    return render(request, "orders/topping.html", context)      

def now_add_topping(request):
    dressing = request.POST["dressing"]
    item_id = int(request.POST["item_id"])
    topping  = request.POST["topping"]
    cartitem =  CartItem.objects.get(pk = item_id)
    
    if dressing == "1 topping":
        if cartitem.toppings.count() >= 1:
            return render(request, "orders/error.html", {"message": "Maximum number of toppings already reached."})            
        else:
          topping_t = Topping.objects.get(topping_name = topping)
          cartitem.toppings.add(topping_t)

    elif dressing == "2 toppings":
        if cartitem.toppings.count() >= 2:
            return render(request, "orders/error.html", {"message": "Maximum number of toppings already reached."})            
        else:
          topping_t = Topping.objects.get(topping_name = topping)
          cartitem.toppings.add(topping_t)      
    
    elif dressing == "3 toppings":
        if cartitem.toppings.count() >= 3:
            return render(request, "orders/error.html", {"message": "Maximum number of toppings already reached."})            
        else:
          topping_t = Topping.objects.get(topping_name = topping)
          cartitem.toppings.add(topping_t)

    else:
        if cartitem.toppings.count() >= 5:
            return render(request, "orders/error.html", {"message": "Maximum number of toppings already reached."})            
        else:
          topping_t = Topping.objects.get(topping_name = topping)
          cartitem.toppings.add(topping_t) 

    return HttpResponseRedirect(reverse("add_topping"))


def delete(request): 
    cartitem_id = int(request.POST["delete"]) 
    cartitem =  CartItem.objects.get(pk = cartitem_id)
    cartitem.delete()
    return HttpResponseRedirect(reverse("cart"))


def order(request, token): 
    firstname = request.user.first_name
    a =  CartItem.objects.filter(created_by = firstname)
    li = []
    for i in a:
        x += i.price
        for topping in i.toppings.all():
             li.append(topping)
        f = OrderItem(user = i.created_by, token = token, category = i.category, dressing=i.dressing, price=i.price, topping = li)
        f.save() 
        li.clear()
    a.delete()
    context = {
        "OrderItems": OrderItem.objects.all(),
        "Total": x
     }  
    return render(request, "orders/order.html", context, {"message": "You have successfully placed an order."})

def checkout(request, **kwargs): 
   firstname = request.user.first_name
   a =  CartItem.objects.filter(created_by = firstname)  
   x = 0
   for i in a:
         x += i.price
   total = x           
   #client_token = generate_client_token()
   publishKey = ''


   if request.method == 'POST':
        
            try:
                token = request.POST.get('stripeToken', False)
                charge = stripe.Charge.create(
                    amount= total,
                    currency='usd',
                    description='Example charge',
                    source=token,
                )

                return HttpResponseRedirect(reverse("order",
                        kwargs={
                            'token': token
                        })
                    )
            except stripe.CardError as e:
                message.info(request, "Your card has been declined.")
        
           
   context = {
        'CartItems': a,
        'total': total,
        'STRIPE_PUBLISHABLE_KEY': publishKey
    }

   return render(request, 'orders/checkout.html', context)        
