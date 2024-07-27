# from . import views
from .views import *
from django.urls import path

urlpatterns = [
      path('', home, name='home'),
      path('forms/login', login, name='login'),
      path('forms/signup', signup, name='signup'),
      path('logout', logout_user, name='logout'),
      path('product/<int:id>',productview, name="productview"),
      path('forms/changepassword', changepassword, name='changepassword'),
      path('add_to_cart/',add_to_cart, name='add_to_cart'),
      path('cart/',cart, name='cart'),
      path('remove_from_cart/',remove_from_cart,name='remove_from_cart'),
      path('contactus/', contactus, name='contactus'),
      path('myorder/', myorder, name='myorder'),
      path('checkout/', checkout, name='checkout'),
      path('confirmation/', confirmation, name='confirmation'),
      path('plus_in_cart/',plus_in_cart,name="plus_in_cart"),
      path('minus_in_cart/',minus_in_cart,name="minus_in_cart"),




 ]

