# Generated by Django 4.2.7 on 2024-02-18 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='static/images/no_photo.jpg', upload_to='profile_pic/'),
        ),
    ]