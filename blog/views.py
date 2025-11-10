from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Post, Profile
from .forms import PostForm, UserUpdateForm, ProfileUpdateForm

# 🏠 Home Page – List all posts
def home(request):
    posts = Post.objects.filter(published=True).order_by('-date_posted')
    return render(request, 'blog/home.html', {'posts': posts})

# 📝 Create New Post
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "✅ Post created successfully!")
            return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, "⚠️ Please fix the errors below.")
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

# 📄 View Post Detail
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# ✏️ Edit Existing Post
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Post updated successfully!")
            return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, "⚠️ Please fix the errors below.")
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

# 🗑️ Delete Post
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "🗑️ Post deleted successfully!")
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

# 👤 Profile View & Edit
@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)

    if request.user == user:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, "✅ Your profile has been updated successfully!")
                return redirect('profile', username=request.user.username)
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=profile)
    else:
        u_form = None
        p_form = None

    context = {'user_obj': user, 'profile': profile, 'u_form': u_form, 'p_form': p_form}
    return render(request, 'blog/profile.html', context)

# 🆕 User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "✅ Your account has been created successfully!")
            return redirect('home')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})
