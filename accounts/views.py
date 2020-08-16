from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Customer, Order
from .forms import OrderForm

# Create your views here.


def home(request):
    order = Order.objects.all()
    customer = Customer.objects.all()

    total_order = order.count()
    delivered = order.filter(status='Delivered').count()
    pending = order.filter(status='Pending').count()
    context = {
        'orders': order,
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


def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form,
        'create': 'Create Order',
    }
    return render(request, 'accounts/orderForm.html', context)


def updateOrder(request, pk):
    order = get_object_or_404(Order, id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form,
        'update': 'Update Order',
    }
    return render(request, 'accounts/orderForm.html', context)


def deleteOrder(request, id):
    order = get_object_or_404(Order, id=id)
    order.delete()
    return redirect('home')
