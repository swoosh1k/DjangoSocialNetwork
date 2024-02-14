from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from .forms import *
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import *
from .tokens import account_activation_token
from django.shortcuts import get_object_or_404

from django.urls import reverse
from django.http import HttpResponseRedirect

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
        you_might_know = User.objects.exclude(id__in = user_followings)
        context = {"posts": posts, 'user': user, 'user_followings': user_followings,
                   'request_user_list': request_user_list, 'you_might_know': you_might_know}
        return render(request, 'social/index.html', context=context)







def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('index')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('social/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
                received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

def register(request):
    if request.method == 'POST':
        form =  UserRegistretion(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            login(request, user)
    else:
        form  = UserRegistretion()
    return render(request, 'social/register.html', context = {'form': form})




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
    form_class = UserChange
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




def Save_post_with_image(request):
    image = request.FILES['image']
    Post.objects.create(context_image =  image, creater = request.user, context_text = request.POST.get('text'))
    return redirect('index')





def Likes(request):
    posts = request.user.likes.all()
    user = request.user
    follower = Follower.objects.get(user = user)
    user_followings = follower.followings.all()
    you_might_know = User.objects.exclude(id__in = user_followings)
    context = {"posts": posts, 'user': user, 'user_followings': user_followings,
               'you_might_know': you_might_know}

    return render(request, 'social/index.html', context = context)



def Bookmarks(request):
    posts = request.user.savers.all()
    user = request.user
    follower = Follower.objects.get(user = user)
    user_followings = follower.followings.all()
    you_might_know = User.objects.exclude(id__in = user_followings)
    context = {"posts": posts, 'user': user, 'user_followings': user_followings,
               'you_might_know': you_might_know}

    return render(request, 'social/index.html', context = context)


def delete_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        return redirect('index')

    return render(request, 'social/delete_profile.html', {'user': user})

def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user_profile', kwargs={'pk': user_id}))
    else:
        form = UserForm(instance=user)

    return render(request, 'social/edit_profile.html', {'form': form, 'user': user})