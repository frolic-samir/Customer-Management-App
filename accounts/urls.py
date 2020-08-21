from django.urls import path
from django.contrib.auth import views as auth_view

from . import views as v

urlpatterns = [
    path('register/', v.register, name='register'),
    path('login/', v.loginPage, name='login'),
    path('logout/', v.logoutPage, name='logout'),

    path('', v.home, name='home'),
    path('user/', v.user, name='user'),

    path('account/', v.account_setting, name='account'),

    path('products/', v.products, name='products'),

    path('customer/<int:customer_id>/', v.customer, name='customer'),
    path('create_order/<str:id>/', v.createOrder, name='create_order'),
    path('update_order/<str:pk>/', v.updateOrder, name='update_order'),
    path('delete_order/<str:id>/', v.deleteOrder, name='delete_order'),

    path('reset_password/', auth_view.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='password_reset'),
    path('reset_password/done/', auth_view.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='accounts/reset_complete.html'),
         name='password_reset_complete'),

]
