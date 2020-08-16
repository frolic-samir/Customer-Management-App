from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home, name='home'),
    path('products/', v.products, name='products'),
    path('customer/<int:customer_id>/', v.customer, name='customer'),

    path('create_order/', v.createOrder, name='create_order'),
    path('update_order/<str:pk>/', v.updateOrder, name='update_order'),

    path('delete_order/<str:id>/', v.deleteOrder, name='delete_order'),
]
