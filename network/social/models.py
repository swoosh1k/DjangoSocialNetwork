from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone


'''Класс юзера'''
class User(AbstractUser):
    bio = models.TextField(max_length = 170, blank = True, null = True )
    profile_pic = models.ImageField(upload_to='profile_pic/', default='static/images/no_photo.jpg', null = True )
    cover = models.ImageField(upload_to = 'covers/', blank = True)
    private = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.username

class PaymentStatus(models.Model):
    User = models.ForeignKey(User, on_delete = models.CASCADE)
    payment_id = models.CharField('id платежа', max_length=500)
    is_payed = models.BooleanField()


    def __str__(self):
        return f'{self.is_payed} платеж от пользователя {self.User}'

class Subscribe(models.Model):
    Users  = models.ManyToManyField(User, null = True, blank = True)
    title = models.CharField('Название подписки', max_length=150)


    def __str__(self):
        return self.title

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



class Group_post(models.Model):
    image = models.ImageField(upload_to =  'Group_post/', null = True)
    context = models.TextField('post text', max_length=3000)
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_posts')
    data_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Group_post  id: {self.id}'

    class Meta:
        verbose_name = 'Group_post'
        verbose_name_plural = 'Group_posts'
        ordering = ['data_created', ]


class Group(models.Model):
    user_created = models.OneToOneField(User, on_delete = models.PROTECT)
    title = models.CharField('group_title', max_length=100)
    users = models.ManyToManyField(User, related_name = 'user_groups', blank = True)
    group_post = models.ManyToManyField(Group_post, related_name = 'post_group', blank = True, null = True )
    bio = models.TextField('описание группы', blank = True)
    data_created = models.DateTimeField(auto_now_add=True)
    group_image = models.ImageField(upload_to='groups/')

    def __str__(self):
        return f'Group {self.title}  id: {self.id}'


    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        ordering = ['data_created',]





class News(models.Model):
    title = models.CharField(max_length=150)
    users = models.ManyToManyField(User, null = True, blank = True)

    def __str__(self):
        return f'News {self.title}'
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'





