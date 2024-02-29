# Generated by Django 4.2.7 on 2024-02-21 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_alter_user_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='group_title')),
                ('bio', models.TextField(blank=True, verbose_name='описание группы')),
                ('data_created', models.DateTimeField(auto_now_add=True)),
                ('posts', models.ManyToManyField(blank=True, null=True, related_name='post_group', to='social.post')),
                ('user_created', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(blank=True, related_name='user_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
                'ordering': ['data_created'],
            },
        ),
    ]