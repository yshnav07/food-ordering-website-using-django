from django.urls import path
from .views import register,login_user,index,restaurent,rest_home,admin,rest_details,menu_details,menu_home,update_rest,cart,add_cart,delete_cart,payment,payment_succes

urlpatterns = [
    path('',index,name='home'),
    path('reg',register,name='register'),
    path('login',login_user,name='login'),
    path('restaurent',restaurent,name='restaurent'),
    path('rest_home',rest_home,name='rest_home'),
    path('admin',admin,name='admin'),
    path('rest_details',rest_details,name='rest_details'),
    path('menu_details',menu_details,name='menu_details'),
    path('menu_home/<int:rest>',menu_home,name='menu_home'),
    path('update_rest/<int:rest>',update_rest,name='update_rest'),
    path('cart',cart,name='cart'),
    path('add_cart/<int:menu>/',add_cart,name='add_cart'),
    path('delete_cart/<int:menu>',delete_cart,name='delete_cart'),
    path('payment',payment,name='payment'),
    path('payment_succes',payment_succes,name="payment_succes")
    #  path('cart/update/<int:menu>/', update_cart, name='update-cart'),
]
