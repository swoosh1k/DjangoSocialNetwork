from celery import shared_task
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from datetime import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import News, Follower, Post, User

'''Task, that shows you last friends posts'''
@shared_task
def send_email_task():
    users = News.objects.first().users.all()
    for user in users:
        follower = Follower.objects.get(user_id = user.id)
        followings = follower.followings.all()
        all_posts = []
        for man in followings:
            post = Post.objects.filter(creater_id = man.id).order_by('data_created')
            if post.exists():
                post = post.last()
                all_posts.append(post)
        all_posts = all_posts[:3]
        print(all_posts)
        subject = 'Новая новость!'
        message = render_to_string('social/send_news_spam.html', {
            'posts': all_posts,
            'user': user
        })
        email = EmailMessage(subject, message, to=[user.email])
        if email.send():
            print(f"Email sent at {datetime.now()} to {user.email}")

'''Task, that counts days until user profile delete '''
@shared_task
def days_until_delete_profile():
    profiles = User.objects.filter(deleted = True)
    for profile in profiles:
        profile.days_until_delete -= 1
        if profile.days_until_delete == 0:
            profile.delete()
        else:
            profile.save()

