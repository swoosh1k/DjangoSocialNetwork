from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import get_object_or_404
from .models import User


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



