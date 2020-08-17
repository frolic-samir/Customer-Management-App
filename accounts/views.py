from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Customer, Order
from .forms import OrderForm
from django.forms import inlineformset_factory
from .filter import filterQuerySet

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
    customer = get_object_or_404(Customer, pk=customer_id)
    orders = customer.order_set.all()
    orders_count = orders.count()
    searchForm = OrderForm()
    if request.GET.get('product') or request.GET.get('status'):
        product = request.GET.get('product')
        status = request.GET.get('status')
        filter_obj = filterQuerySet(
            product=product, status=status, order_set=orders)
        orders = filter_obj.querySearch()
        searchForm = OrderForm(initial={'product': product, 'status': status})

    context = {
        'form': searchForm,
        'customer': customer,
        'orders': orders,
        'orders_count': orders_count,
    }
    return render(request, 'accounts/customers.html', context)


def createOrder(request, id):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=2)
    customer = get_object_or_404(Customer, id=id)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        # form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context = {
        'formset': formset,
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
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    context = {
        'item': order.product
    }
    return render(request, 'accounts/deleteOrder.html', context)
