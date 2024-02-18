from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views
from django.contrib.auth.views import LogoutView



urlpatterns =  [
    path('', messages, name = 'messages')
]





urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
