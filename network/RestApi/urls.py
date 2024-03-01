from django.contrib import admin
from django.urls import path, include
from .views import PostView, UserView
urlpatterns = [
    path('', PostView.as_view(), name = 'post-list'),
    path('userApi/', UserView.as_view(), name = 'user-list')

]