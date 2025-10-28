from django import forms
from .models import Post, Comment, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# ------------------------------
# Post Form
# ------------------------------
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'published']


# ------------------------------
# Comment Form
# ------------------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


# ------------------------------
# User Registration Form
# ------------------------------
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# ------------------------------
# Profile Form
# ------------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']


# ------------------------------
# Profile Edit Forms
# ------------------------------
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'location']
