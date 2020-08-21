from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth import login, logout, authenticate, models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Customer, Order
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filter import filterQuerySet
from .decorator import unauthenticate_user, allowed_user, admin_only

# Create your views here.


@unauthenticate_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('login')
    context = {}
    return render(request, 'accounts/login.html', context)


@unauthenticate_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
@allowed_user(allowed_one=['admin'])
def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_user(allowed_one=['admin'])
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


@login_required(login_url='login')
@allowed_user(allowed_one=['admin'])
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


@login_required(login_url='login')
@allowed_user(allowed_one=['admin'])
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


@login_required(login_url='login')
@allowed_user(allowed_one=['admin'])
def deleteOrder(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    context = {
        'item': order.product
    }
    return render(request, 'accounts/deleteOrder.html', context)


@login_required
@allowed_user(allowed_one=['customer'])
def user(request):
    orders = request.user.customer.order_set.all()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'total_order': total_order,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/user.html', context)


def account_setting(request):
    user = request.user.customer
    form = CustomerForm(instance=user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {
        'form': form
    }
    return render(request, 'accounts/account.html', context)
