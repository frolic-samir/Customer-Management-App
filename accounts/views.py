from django.shortcuts import render, get_object_or_404
from .models import Product, Customer, Order

# Create your views here.


def home(request):
    order = Order.objects.all()
    customer = Customer.objects.all()

    total_order = order.count()
    delivered = order.filter(status='Delivered').count()
    pending = order.filter(status='Pending').count()
    context = {
        'order': order,
        'customer': customer,
        'total_order': total_order,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)


def customer(request, customer_id):
    # customer = Customer.objects.get(pk=customer_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    orders = customer.order_set.all()
    orders_count = orders.count()
    context = {
        'customer': customer,
        'orders': orders,
        'orders_count': orders_count,
    }
    return render(request, 'accounts/customers.html', context)
