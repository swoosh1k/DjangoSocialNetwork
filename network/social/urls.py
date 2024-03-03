from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views
from django.contrib.auth.views import LogoutView
from .views import create_group


urlpatterns = [
    path('', index, name = 'index'),
    path('adminq/', admin.site.urls, name='admin'),
    path('social/login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('register/', register, name = 'register'),
    path('subscribe/', Subscribe_on_user, name = 'subscribe'),
    path('unsubscribe/<int:pk>/', UnSubscribe, name = 'unsubscribe'),
    path('addlike/', AddLike, name = 'add_like'),
    path('profile/<int:pk>/', UserProfile.as_view(), name = 'user_profile'),
    path('followings/', Followings, name = 'followings'),
    path('post_create_text/',Post_create_contex , name = 'post_context_create'),
    path('delete_post/', DeletePost, name = 'delete_post'),
    path('savepost/', Save_post, name = 'save_post'),
    path('add_comment/<int:pk>/', Add_comment , name = 'add_comment'),
    path('save_post_with_image/', Save_post_with_image, name = 'save_post_with_image'),
    path('likes/', Likes, name =  'likes'),
    path('saves/', Bookmarks, name = 'saves'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('delete_profile/<int:user_id>/', delete_profile, name='delete_profile'),
    path('edit_profile/<int:user_id>/', edit_profile, name='edit_profile'),
    path('people_search/', search_results_view, name = 'people-search'),
    path('thread_start/<int:pk>/', thread_start, name = 'thread_start'),
    path('groups/', Groups_all, name = 'groups'),
    path('group_search/', Group_search, name  = 'group_search'),
    path('group/<int:pk>/', Group_detail.as_view(), name = 'group'),
    path('buy-subscribe/', Buy_Subscribe, name = 'buy_subscribe'),
    path('pay/', create_payment, name = 'pay'),
    path('payment/notification/', yookassa_webhook, name='yookassa_webhook'),

    path('save_group_post/<int:pk>/', save_group_post, name = 'save_group_post'),
    path('create_group/', create_group, name='create_group'),
    path('delete_group/<int:group_id>/', delete_group, name='delete_group'),



    path('subscribe_on_news/', subscribe_on_news, name = 'subscribe_on_news'),
    path('confirm_subscribe_on_news/', confirm_subscribe_on_news, name = 'confirm_subscribe_on_news'),
    path('unsubscribe_on_news/', unsubscribe_on_news, name = 'unsubscribe_on_news'),
    path('delete_profile_as_moderator/<int:pk>/', delete_profile_moderator, name = 'delete_profile_moderator'),
    path('add_moderator/', add_moderator, name = 'add_moderator')

]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
