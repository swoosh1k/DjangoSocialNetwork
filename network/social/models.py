from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


'''Класс юзера'''
class User(AbstractUser):
    bio = models.TextField(max_length = 170, blank = True, null = True )
    profile_pic = models.ImageField(upload_to='profile_pic/')
    cover = models.ImageField(upload_to = 'covers/', blank = True)
    private = models.BooleanField(default=False, blank=True)







    def __str__(self):
        return self.username
'''Класс постов'''
class Post(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "posts")
    data_created = models.DateTimeField(default = timezone.now)
    context_text = models.TextField(max_length=150, blank = True)
    context_image = models.ImageField(upload_to='posts/', blank  = True)
    likers = models.ManyToManyField(User, blank = True, related_name="likes")
    savers = models.ManyToManyField(User, blank = True, related_name = 'savers')
    comment_count = models.IntegerField(default = 0)

    def __str__(self):
        return f'Post ID : {self.id} creater: {self.creater}'


    def img_url(self):
        return self.context_image.url

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"




    @property
    def total_likes(self):
        return self.likers.count()





'''Класс комментариев'''
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenters')
    comment_content = models.TextField(max_length=78)
    comment_time = models.DateTimeField(default = timezone.now)


    def __str__(self):
        return f'{self.post} Commenter : {self.commenter}'

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


'''Класс подписчика'''
class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followings = models.ManyToManyField(User, blank = True, related_name = 'followers')

    def __str__(self):
        return f'User: {self.user}'


    class Meta:
        verbose_name = "Follower"
        verbose_name_plural = "Followers"


'''Класс для запрасов(для частных профилей)'''
class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_from')
    requests = models.ManyToManyField(User, blank = True, related_name = 'requests')
