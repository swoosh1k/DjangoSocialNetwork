from django.contrib import admin
from django.urls import path, include
from .views import getView, PostUpdateView
urlpatterns = [
    path('', getView.as_view(), name = 'post-list'),
    path('posts/<int:pk>/', PostUpdateView.as_view(), name='post-update'),

]