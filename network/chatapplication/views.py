from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Thread
# Create your views here.



@login_required
def messages(request):
    threads  = Thread.objects.by_user(user = request.user).prefetch_related('chatmessage_thread')
    context = {
        'Threads': threads
    }
    return render(request, 'chatapplication/messages.html', context = context)