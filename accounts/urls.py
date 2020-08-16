from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home, name='home'),
    path('products/', v.products, name='products'),
    path('customer/<int:customer_id>/', v.customer, name='customer'),
]
