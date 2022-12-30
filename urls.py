from spa import views
from django.urls import path,include
from .views import index,about,signup,signin,gallery,service,contact,pricing
from .views import coffee_payment, payment_status

urlpatterns = [
    path('',index),
    path('about.html',about),
    path('gallery.html',gallery),
    path('service.html',service),
    path('contact.html',contact),
    path('pricing.html',pricing),
    path('signup/',views.signup, name = "signup"),
    path('signin/',views.signin, name = "signin"),
    path('coffee_payment',coffee_payment,name='coffee-payment'),
    path('payment_status',payment_status,name='payment-status'),
]
