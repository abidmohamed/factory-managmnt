from django.http import HttpResponse
from django.shortcuts import redirect


def unauthneticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not allowed')

            return view_func(request, *args, **kwargs)

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('family:family_list')
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('accounts:login')

    return wrapper_func


def customer_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return view_func(request, *args, **kwargs)
        if group == 'admin':
            return redirect('accounts:home')
        else:
            return redirect('accounts:login')

    return wrapper_func
