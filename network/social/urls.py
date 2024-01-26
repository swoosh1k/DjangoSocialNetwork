from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name = 'index'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('subscribe/<int:pk>/', Subscribe, name = "subscribe"),
    path('unsubscribe/<int:pk>/', UnSubscribe, name = 'unsubscribe'),
    path('addlike/<int:pk>/', AddLike, name = 'add_like'),
    path('remove_like/<int:pk>/', Remove_like, name  = 'remove_like')

]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)