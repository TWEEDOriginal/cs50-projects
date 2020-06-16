from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("signup", views.signup_view, name="signup"),
    path("logout", views.logout_view, name="logout"),
    path("cart", views.cart, name="cart"),
    path("rs", views.add_r_s_to_cart, name="add_r_s_to_cart"),
    path("rl", views.add_r_l_to_cart, name="add_r_l_to_cart"),
    path("ss", views.add_s_s_to_cart, name="add_s_s_to_cart"),
    path("sl", views.add_s_l_to_cart, name="add_s_l_to_cart"),
    path("Ss", views.add_Sub_s_to_cart, name="add_Sub_s_to_cart"),
    path("Sl", views.add_Sub_l_to_cart, name="add_Sub_l_to_cart"),
    path("p", views.add_p_to_cart, name="add_p_to_cart"),
    path("Sa", views.add_salad_to_cart, name="add_salad_to_cart"),
    path("ds", views.add_d_s_to_cart, name="add_d_s_to_cart"),
    path("dl", views.add_d_l_to_cart, name="add_d_l_to_cart"),
    path("add_topping", views.add_topping, name="add_topping"),
    path("now_add_topping", views.now_add_topping, name="now_add_topping"),
    path("delete", views.delete, name="delete"),
    path("checkout", views.checkout, name="checkout"),
    path("order", views.order, name="order")
]
