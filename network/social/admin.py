from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Follower, Comment, User, Request, Group, Subscribe, PaymentStatus, News, Group_post
class PostAdmin(admin.ModelAdmin):
    list_display = ['creater', 'data_created', 'context_text', 'comment_count']
    list_filter = ['data_created']
    search_fields = ['creater__username', 'context_text']

class FollowerAdmin(admin.ModelAdmin):
    list_display = ['user']
    filter_horizontal = ['followings']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'commenter', 'comment_time']
    list_filter = ['comment_time']
    search_fields = ['post__id', 'commenter__username']

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name',  'last_name', 'get_profile_pic_display', 'get_cover_display', 'last_login', 'is_superuser', 'is_staff', 'is_active']
    search_fields = ['username', 'first_name', 'email']
    list_filter = ['is_superuser', 'is_staff', 'is_active']

    def get_profile_pic_display(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />'.format(obj.profile_pic.url))
        else:
            return 'Нет изображения'

    def get_cover_display(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />'.format(obj.cover.url))
        else:
            return 'Нет изображения'

    get_profile_pic_display.short_description = 'Profile Picture'
    get_cover_display.short_description = 'Cover'

class RequestAdmin(admin.ModelAdmin):
    list_display = ['user']
    filter_horizontal = ['requests']


admin.site.register(News)
admin.site.register(PaymentStatus)
admin.site.register(Subscribe)
admin.site.register(Group)
admin.site.register(Post, PostAdmin)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Request, RequestAdmin)
