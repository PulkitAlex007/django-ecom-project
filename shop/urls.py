from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("select/<int:id>/",views.select,name="select"),
    path("add-to-cart/",views.add_to_cart,name="add_to_cart"),
    path("cart/",views.cart,name="cart"),
    path("cart/",views.showCart,name="showCart"),
    path("cart/increase/", views.increase_qty, name='increase_qty'),
    path('cart/decrease/', views.decrease_qty, name='decrease_qty'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path('add/', views.add_product, name='add_product'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path("place-order/", views.place_order, name="place_order"),
    path("order-success/", views.order_success, name="order_success"),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('logout/', views.logout_view, name='logout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart_and_redirect, name='add_to_cart_and_redirect'),
]

