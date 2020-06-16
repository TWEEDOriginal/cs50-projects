def add_to_cart(request): 
    
        price = request.POST["price"]
        if price == "small_regular_pizza":
            try:    
               r_s_price = float(request.POST["r_s_price"])
               food = Regular_pizza.objects.get(small_price=r_s_price)
               category = "Regular Pizza"
               price =food.small_price
            except KeyError:    
                   return render(request, "orders/error.html", {"message": "No selection."})          
            except Regular_pizza.DoesNotExist:    
                   return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."})
       

        elif price == "large_regular_pizza":
            try:    
               r_l_price = float(request.POST["r_l_price"])
               food = Regular_pizza.objects.get(large_price=r_l_price)
               category = "Regular Pizza"
               price =food.large_price
            except KeyError:    
                   return render(request, "orders/error.html", {"message": "No selection."})          
            except Regular_pizza.DoesNotExist:    
                   return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."})
        
        elif price == "small_sicilian_pizza":
            try:    
               s_s_price = float(request.POST["s_s_price"])
               food = Sicilian_pizza.objects.get(small_price=s_s_price)
               category = "Sicilian pizza"
               price =food.small_price
            except KeyError:    
                   return render(request, "orders/error.html", {"message": "No selection."})          
            except Sicilian_pizza.DoesNotExist:    
                   return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."})
         

        elif price == "large_sicilian_pizza":
            try:    
               s_l_price = float(request.POST["s_l_price"])
               food = Sicilian_pizza.objects.get(large_price=s_l_price)
               category = "Sicilian pizza"
               price =food.large_price
            except KeyError:    
                   return render(request, "orders/error.html", {"message": "No selection."})          
            except Sicilian_pizza.DoesNotExist:    
                   return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."}) 
        

        elif price == "small_sub":
            try:    
               Sub_s_price = int(request.POST["Sub_s_price"])
               food = Sub.objects.get(pk=Sub_s_price)
               category = "Sub"
               price =food.small_price
            except KeyError:    
                   return render(request, "orders/error.html", {"message": "No selection."})          
            except Sub.DoesNotExist:    
                   return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."}) 
        

        elif price == "large_sub":
            try:    
               Sub_l_price = int(request.POST["Sub_l_price"])
               food = Sub.objects.get(pk=Sub_l_price)
               category = "Sub"
               price =food.large_price
            except KeyError:    
                   return render(request, "orders/error.html", {"message": "No selection."})          
            except Sub.DoesNotExist:    
                   return render(request, "orders/error.html", {"message": "No pizza with this name exists in our database."}) 

        
        f = CartItem(category = category, dressing=food.dressing, price= price) 
        f.save()     
        return HttpResponseRedirect(reverse("index"))