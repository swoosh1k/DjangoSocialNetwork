from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name = 'index'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('register/', register, name = 'register'),
    path('subscribe/', Subscribe, name = "subscribe"),
    path('unsubscribe/<int:pk>/', UnSubscribe, name = 'unsubscribe'),
    path('addlike/', AddLike, name = 'add_like'),
    path('remove_like/<int:pk>/', Remove_like, name  = 'remove_like'),
    path('send_request/<int:pk>/', SendRequest, name = 'send_request'),
    path('profile/<int:pk>/', UserProfile.as_view(), name = 'user_profile'),
    path('confirm_request/<int:pk>/', ConfirmRequest, name = 'request_confirm'),
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

]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
