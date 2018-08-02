from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("shoppingCart", views.shoppingCart, name="shoppingCart"),
    path("checkout", views.checkout, name="checkout"),
    path("manage", views.manage, name="manage"),
    path("addTopping", views.addTopping, name="addTopping")
]
