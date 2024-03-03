from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import get_object_or_404
from .models import User
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy

def moderator_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='Moderators').exists():
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied('You are not moderator and you could not  do this')
    return _wrapped_view


def user_is_request_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user == get_object_or_404(User, id = kwargs['user_id']):
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied('You are not this user and you could not do this')
    return _wrapped_view


def is_admin_or_moderator(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Модераторы').exists())

def admin_or_moderator_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: is_admin_or_moderator(u),
        login_url=reverse_lazy('login')  # URL для перенаправления в случае отсутствия доступа
    )(view_func)
    return decorated_view_func

def admin_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied('You are not this user and you could not do this')

    return _wrapped_view


