from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Comment, Category, Profile
from .forms import PostForm, CommentForm, ProfileUpdateForm, UserUpdateForm



# ------------------------------
# Home / Post List
# ------------------------------
def home(request):
    posts = Post.objects.filter(published=True).order_by('-date_posted')
    categories = Category.objects.all()
    return render(request, 'blog/home.html', {'posts': posts, 'categories': categories})


# ------------------------------
# Post Detail View
# ------------------------------
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user if request.user.is_authenticated else None
            new_comment.save()
            messages.success(request, "Your comment has been added!")
            return redirect('post-detail', slug=slug)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })


# ------------------------------
# Create a New Post
# ------------------------------
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your post has been created successfully!")
            return redirect('post-detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


# ------------------------------
# Edit Post (for pk-based URLs)
# ------------------------------
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post edited successfully!")
            return redirect('post-detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form})


# ------------------------------
# Update Post (for slug-based URLs)
# ------------------------------
@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('post-detail', slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('post-detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


# ------------------------------
# Delete Post
# ------------------------------
@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('post-detail', slug=slug)
    post.delete()
    messages.success(request, "Post deleted successfully!")
    return redirect('home')


# ------------------------------
# Filter Posts by Category
# ------------------------------
def posts_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, published=True)
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})


# ------------------------------
# User Registration
# ------------------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


# ------------------------------
# Profile View
# ------------------------------
@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(author=user)
    return render(request, 'blog/profile.html', {'profile': profile, 'posts': posts})


# ------------------------------
# Edit Profile
# ------------------------------
@login_required
def edit_profile(request):
    # Get the current user's profile
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        # Create two forms: one for User, one for Profile
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        # Check if both forms are valid
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # GET request: pre-fill the forms with current data
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    
    # Pass both forms to the template
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog/edit_profile.html', context)

