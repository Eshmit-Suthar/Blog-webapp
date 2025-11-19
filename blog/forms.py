from django import forms
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from .models import Post, Comment, Profile, Message


# ----------------------------
# 📝 Post Creation / Edit Form
# ----------------------------
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label="Post Content")
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'category', 'image', 'published', 'background_color', 'background_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title',
                'maxlength': 200
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add comma-separated tags'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'background_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # Add a color input for background_color
    background_color = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control', 'value': '#ffffff'}),
        label='Background Color'
    )


# ----------------------------
# 💬 Comment Form
# ----------------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment...',
                'rows': 3
            }),
        }


# ----------------------------
# 👤 Profile Edit Form
# ----------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write something about yourself...',
                'rows': 3
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# ----------------------------
# ⚙️ User & Profile Update Forms
# ----------------------------
class UserUpdateForm(forms.ModelForm):
    """Form for updating basic User info"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating profile details"""
    class Meta:
        model = Profile
        fields = ['bio', 'image']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write something about yourself...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


# ----------------------------
# 💌 Messaging Form
# ----------------------------
class MessageForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Type your message...'
        }),
        label=''
    )

    class Meta:
        model = Message
        fields = ['body']
