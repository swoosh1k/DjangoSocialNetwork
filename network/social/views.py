from django.contrib import messages
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
from django.views.generic import CreateView, UpdateView, DetailView

from .models import *




def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        followers = Follower.objects.filter(user = request.user)
        Tequest = Request.objects.filter(user = request.user)
        if not followers.exists():
            Follower.objects.create(user = request.user)
            follower = followers.first()
            user_followings = follower.followings.all()
        else:
            follower = followers.first()
            user_followings = follower.followings.all()
        if not Tequest.exists():
            Request.objects.create(user = request.user)
            teuqest = Tequest.first()
            request_user_list = teuqest.requests.all()
        else:
            teuqest = Tequest.first()
            request_user_list = teuqest.requests.all()
        user = request.user
        posts = Post.objects.all()
        context = {"posts": posts, 'user': user, 'user_followings': user_followings,
                   'request_user_list': request_user_list}
        return render(request, 'social/index.html', context=context)




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







class UserLogin(LoginView):
    form_class = UserLogin
    template_name = 'social/login.html'
    model = User


    def get_context_data(self,*, object_list  = None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] =  'login'
        return context



class UserProfile(UpdateView):
    model = User
    context_object_name = 'user'
    template_name = 'social/settings.html'
    form_class = UserChange
    def get_context_data(self,*, object_list = None,  **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = f'Profile {self.object}'
        context['form'] = UserChange
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




def SendRequest(request, pk):
    user = request.user
    user_request_to = User.objects.get(id = pk)
    Tequest = Request.objects.get(user = user)
    Tequest.requests.add(user_request_to)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])




def ConfirmRequest(request, pk):
    user_from = User.objects.get(id = pk)
    Tequest = Request.objects.get(user = user_from)
    Tequest.requests.remove(request.user)
    follow = Follower.objects.get(user = user_from)
    follow.followings.add(request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


