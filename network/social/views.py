from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from .forms import *
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.decorators.csrf import ensure_csrf_cookie

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
        my_list = []
        you_might_know = User.objects.exclude(id__in = user_followings)
        context = {"posts": posts, 'user': user, 'user_followings': user_followings,
                   'request_user_list': request_user_list, 'you_might_know': you_might_know}
        return render(request, 'social/index.html', context=context)



class RegisterView(CreateView):
    success_url = reverse_lazy('login')
    model = User
    form_class = UserRegistretion
    template_name =  'social/register.html'

    def get_context_data(self,*, object_list = None , **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rgistretion'
        return context




class UserLogin(LoginView):
    form_class = UserLogin
    template_name = 'social/login.html'
    model = User

    def get_context_data(self,*, object_list  = None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] =  'login'
        return context



class UserProfile(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'social/profile.html'

    def get_context_data(self,*, object_list = None,  **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = f'Profile {self.object}'
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




def AddLike(request):
    if request.POST.get('action') == 'post':
        checker = None
        post_id  = int(request.POST.get('post_id'))
        post = get_object_or_404(Post , id = post_id)
        if post.likers.filter(id = request.user.id).exists():
            post.likers.remove(request.user)
            post.save()
            checker = 0

        else:
            post.likers.add(request.user)
            post.save()
            checker = 1
        return JsonResponse({'total_likes': post.total_likes, 'check': checker,})
    return HttpResponse('Error acces ')





def Subscribe(request):
    if request.POST.get('action') == 'post':
        flag = None
        creater_id = int(request.POST.get('creater_id'))
        creater = get_object_or_404(User, id = creater_id)
        user = Follower.objects.get(user = request.user)
        if creater in user.followings.all():
            user.followings.remove(creater)
            user.save()
            flag = 1
        else:
            user.followings.add(creater)
            user.save()
            flag = 0
        if flag == 1:
            info  = 'Follow'
        else:
            info = 'Unfollow'

        return JsonResponse({"info": info,})
    return HttpResponse('Error acces ')









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




def Followings(request):
    if request.user:
        follower = Follower.objects.get(user = request.user)
    users_followings = follower.followings.all()
    posts = Post.objects.filter(creater__id__in = users_followings)
    context = {'posts': posts}
    return render(request, 'social/index.html', context = context)




def DeletePost(request):
    pk = request.GET.get('pk')
    post = Post.objects.get(id = pk)
    print(post)
    post.delete()
    return JsonResponse({'deleted': True})




def Save_post(request):
    flag = None
    user = request.user
    post_id = int(request.POST.get('pk'))
    post = Post.objects.get(id = post_id)
    if user in post.savers.all():
        post.savers.remove(request.user)
        post.save()
        flag = 0
    else:
        post.savers.add(request.user)
        post.save()
        flag = 1

    return JsonResponse({'flag': flag })





def Post_create_contex(request):
    Post.objects.create(creater = request.user, context_text = request.POST.get('text'))
    return HttpResponseRedirect(request.META['HTTP_REFERER'])











def Add_comment(request, pk):
    Comment.objects.create(post = Post.objects.get(id = pk), commenter = request.user,comment_content = request.POST.get('comment'))
    return HttpResponseRedirect(request.META['HTTP_REFERER'])




