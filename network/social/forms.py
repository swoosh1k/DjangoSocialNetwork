from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User, Group



class UserLogin(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'Username'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Password'}))

    class Meta:
        model = User
        fields  = ['username', 'password',]


class UserRegistretion(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password again'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username','email',  'password1', 'password2','private',)



class UserChange(UserChangeForm):
    email = forms.EmailField(widget = forms.TextInput(attrs= {'readonly': True}))
    class Meta:
        model = User
        fields = ("profile_pic",)




class UserForm(forms.ModelForm):
    delete_profile_pic = forms.BooleanField(required=False)
    delete_cover = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'private', 'profile_pic', 'cover']
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'multiple': False}),
            'cover': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data['delete_profile_pic']:
            instance.profile_pic.delete()
            instance.profile_pic = None

        if self.cleaned_data['delete_cover']:
            instance.cover.delete()
            instance.cover = None

        if commit:
            instance.save()

        return instance


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'bio', 'group_image']