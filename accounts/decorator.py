from django.http import HttpResponse
from django.shortcuts import redirect, render


def unauthenticate_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_user(allowed_one=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_one:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'accounts/notallowed.html')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrap_fun(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('user')
        elif group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Identify yourself. Invalid user")
    return wrap_fun
