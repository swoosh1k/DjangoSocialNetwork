from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from .forms import *
from django.views.generic import CreateView, UpdateView

from .models import *




def index(request):
    followers = Follower.objects.filter(user = request.user )
    if not followers.exists():
        Follower.objects.create(user = request.user)
        follower = followers.first()
        user_followings = follower.followings.all()
    else:
        follower = followers.first()
        user_followings = follower.followings.all()
    user = request.user
    posts = Post.objects.all()
    if request.user.is_authenticated:
        context =  {"posts": posts, 'user': user, 'user_followings': user_followings}
        return render(request, 'social/index.html', context = context )

    else:
        return redirect('login')




class RegisterView(CreateView):
    model = User
    form_class = UserRegistretion
    success_url = reverse_lazy('login')
    template_name = 'social/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registretion'
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)







class UserLoginView(LoginView):
    template_name = 'social/login.html'
    form_class = UserLogin
    def get_context_data(self,*, object_list = None , **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        return context



class UserProfile(UpdateView):
    model = User
    template_name = 'social/profile.html'
    form_class = UserChange
    def get_context_data(self,*, object_list = None,  **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = f'Profile {self.request.User.username}'
        return context




def Subscribe(request, pk):
    user = request.user
    user_get = User.objects.get(id = pk)
    follower = Follower.objects.get(user = user)
    follower.followings.add(user_get)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])




def UnSubscribe(request, pk):
    user = request.user
    user_get = User.objects.get(id = pk)
    follower = Follower.objects.get(user= user)
    follower.followings.remove(user_get)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])




def AddLike(request, pk):
    post  = Post.objects.get(id = pk)
    post.likers.add(request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])




def Remove_like(request, pk):
    post = Post.objects.get(id = pk)
    post.likers.remove(request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])




