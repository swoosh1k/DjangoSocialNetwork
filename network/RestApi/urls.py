from django.contrib import admin
from django.urls import path, include
from .views import getView, UserView, PostUpdateView
urlpatterns = [
    path('', getView.as_view(), name = 'post-list'),
    path('userApi/', UserView.as_view(), name = 'user-list'),
    path('posts/<int:pk>/', PostUpdateView.as_view(), name='post-update'),

]