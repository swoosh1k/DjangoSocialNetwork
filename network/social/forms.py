from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User



class UserLogin(AuthenticationForm):
    class Meta:
        model = User
        fields  = ['username', 'password',]


class UserRegistretion(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username','email',  'password1', 'password2',)



class UserChange(UserChangeForm):
    username = forms.CharField(widget = forms.TextInput(attrs = {'readonly': True}))
    email = forms.EmailField(widget = forms.TextInput(attrs= {'readonly': True}))
    class Meta:
        model = User
        fields = ("first_name", "last_name", "profile_pic", "username", "email",)
