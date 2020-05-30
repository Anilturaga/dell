from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('foryou/',views.foryou,name="foryou"),
    path('cart/',views.cart,name="cart"),
    path('foryou/<int:index>/single/',views.single,name ="single"),
    path('formHandler',views.formHandler,name="formHandler")
]