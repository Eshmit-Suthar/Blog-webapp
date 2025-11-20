from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import Post, Profile, Message
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from .forms import PostForm, UserUpdateForm, ProfileUpdateForm, MessageForm
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.views.decorators.http import require_GET


# ----------------------------
# 🏠 Home Page
# ----------------------------
def home(request):
    # Show published posts to everyone; if the user is logged in, also include their own posts (including unpublished drafts)
    if request.user.is_authenticated:
        posts = Post.objects.filter(Q(published=True) | Q(author=request.user)).order_by('-date_posted')
    else:
        posts = Post.objects.filter(published=True).order_by('-date_posted')
    # compute draft count for the right-column widget (avoid complex template expressions)
    draft_count = 0
    if request.user.is_authenticated:
        draft_count = Post.objects.filter(author=request.user, published=False).count()
    return render(request, 'blog/home.html', {'posts': posts, 'draft_count': draft_count})


# ----------------------------
# 📝 Create Post
# ----------------------------
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = post.title.lower().replace(' ', '-')[:200]
            post.save()
            messages.success(request, "✅ Post created successfully!")
            return redirect('post_detail', pk=post.pk)
        messages.error(request, "⚠️ Please fix the errors below.")
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


# ----------------------------
# 📄 Post Detail
# ----------------------------
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Handle new comment submissions
    comment_form = None
    if request.method == 'POST' and 'comment' in request.POST:
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect('login')
        from .forms import CommentForm
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment added.")
            return redirect('post_detail', pk=post.pk)
    else:
        from .forms import CommentForm
        comment_form = CommentForm()

    # Absolute URL for sharing
    absolute_url = request.build_absolute_uri(post.get_absolute_url())

    # Like state and count
    liked = request.user.is_authenticated and (request.user in post.likes.all())
    like_count = post.likes.count()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comment_form': comment_form,
        'absolute_url': absolute_url,
        'liked': liked,
        'like_count': like_count,
    })


# ----------------------------
# ✏️ Edit Post
# ----------------------------
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
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


# ----------------------------
# 🗑️ Delete Post
# ----------------------------
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "🗑️ Post deleted successfully!")
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


# ----------------------------
# 👤 Profile View + Follow
# ----------------------------
@login_required
def profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=user_obj)

    u_form = p_form = None

    # Update profile
    if request.user == user_obj:
        if request.method == 'POST' and 'update' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, "✅ Your profile has been updated!")
                return redirect('profile', username=request.user.username)
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=profile)

    # Follow / Unfollow logic
    current_profile, _ = Profile.objects.get_or_create(user=request.user)
    is_following = current_profile in profile.followers.all()

    if request.method == 'POST' and 'follow' in request.POST:
        if current_profile != profile:
            if is_following:
                profile.followers.remove(current_profile)
                messages.info(request, f"You unfollowed {user_obj.username}")
            else:
                profile.followers.add(current_profile)
                messages.success(request, f"You followed {user_obj.username}")
        return redirect('profile', username=username)

    # Allow the profile owner to toggle viewing all their posts (including drafts) via ?all=1
    show_all = (request.user == user_obj and request.GET.get('all') == '1')
    if show_all:
        posts = Post.objects.filter(author=user_obj).order_by('-date_posted')
    else:
        posts = Post.objects.filter(author=user_obj, published=True).order_by('-date_posted')

    # Provide a separate list of all posts for the profile owner (used in 'My Posts' section)
    my_posts = None
    if request.user == user_obj:
        my_posts = Post.objects.filter(author=user_obj).order_by('-date_posted')

    # follower/following counts and lists
    followers_count = profile.followers.count()
    following_count = profile.following.count()

    # Lists of Profile objects for display (convert to user objects in template as needed)
    followers_list = profile.followers.all()
    following_list = profile.following.all()

    return render(request, 'blog/profile.html', {
        'user_obj': user_obj,
        'profile': profile,
        'u_form': u_form,
        'p_form': p_form,
        'is_following': is_following,
        'posts': posts,
        'show_all': show_all,
        'my_posts': my_posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'followers_list': followers_list,
        'following_list': following_list
    })



@login_required
def toggle_follow(request, username):
    """Toggle follow/unfollow for the current user to the target username."""
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        return redirect('profile', username=username)

    current_profile, _ = Profile.objects.get_or_create(user=request.user)
    target_profile, _ = Profile.objects.get_or_create(user=target_user)

    if current_profile in target_profile.followers.all():
        target_profile.followers.remove(current_profile)
        messages.info(request, f"You unfollowed {target_user.username}")
    else:
        target_profile.followers.add(current_profile)
        messages.success(request, f"You followed {target_user.username}")

    # Redirect back to referrer if available, else to target profile
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('profile', username=username)


@login_required
def toggle_publish(request, pk):
    """Toggle published state for a post. Only the author may toggle."""
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "You don't have permission to publish/unpublish this post.")
        return redirect('profile', username=request.user.username)

    if request.method == 'POST':
        post.published = not post.published
        post.save()
        state = 'published' if post.published else 'unpublished'
        messages.success(request, f"Post {state} successfully.")

    # Redirect back to the profile page of the author
    return redirect('profile', username=post.author.username)


def search_posts(request):
    """Search posts by numeric id (redirect to detail) or by title substring."""
    q = request.GET.get('q', '').strip()
    if not q:
        return render(request, 'blog/post_search_results.html', {'query': q, 'posts': []})

    # If q is integer, try redirect to that post by pk
    if q.isdigit():
        try:
            post = Post.objects.get(pk=int(q))
            return redirect('post_detail', pk=post.pk)
        except Post.DoesNotExist:
            # fall through to title search
            pass

    # Only show unpublished posts to their authors; everyone else sees published posts only
    if request.user.is_authenticated:
        posts = Post.objects.filter(title__icontains=q).filter(Q(published=True) | Q(author=request.user))
    else:
        posts = Post.objects.filter(title__icontains=q, published=True)

    return render(request, 'blog/post_search_results.html', {'query': q, 'posts': posts})


def search_all(request):
    """Combined search that returns matching profiles and posts.
    - Profiles: search username, first_name, last_name, or email
    - Posts: title substring matches (only published posts for non-authors)
    """
    q = request.GET.get('q', '').strip()
    # Allow '@username' queries by stripping a leading @ or other common prefix characters
    if q.startswith('@') or q.startswith('#'):
        q = q[1:].strip()

    if q:
        profiles = User.objects.filter(
            Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q)
        )
        if request.user.is_authenticated:
            posts = Post.objects.filter(title__icontains=q).filter(Q(published=True) | Q(author=request.user))
        else:
            posts = Post.objects.filter(title__icontains=q, published=True)
    else:
        profiles = User.objects.none()
        posts = Post.objects.none()

    return render(request, 'blog/search_all_results.html', {'query': q, 'profiles': profiles, 'posts': posts})


# ----------------------------
# 🆕 Register
# ----------------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "✅ Account created successfully!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


# ----------------------------
# 🔍 Search Profiles
# ----------------------------
@login_required
def search_profiles(request):
    query = request.GET.get('q', '').strip()
    if query.startswith('@') or query.startswith('#'):
        query = query[1:].strip()
    results = User.objects.filter(username__icontains=query) if query else []
    return render(request, 'blog/search.html', {'results': results, 'query': query})


@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            messages.info(request, 'You unliked the post.')
        else:
            post.likes.add(request.user)
            messages.success(request, 'You liked the post.')
    return redirect('post_detail', pk=pk)


@login_required
@require_POST
def toggle_like_ajax(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})


@login_required
@require_POST
def add_comment_ajax(request, pk):
    post = get_object_or_404(Post, pk=pk)
    body = request.POST.get('body', '').strip()
    if not body:
        return JsonResponse({'error': 'Empty comment'}, status=400)
    comment = None
    from .models import Comment
    comment = Comment.objects.create(post=post, author=request.user, body=body)
    # Render single comment HTML to return
    # include `request` in context so the partial can reflect the current user's liked state
    html = render_to_string('blog/_comment.html', {'comment': comment, 'request': request})
    return JsonResponse({'success': True, 'comment_html': html, 'comment_count': post.comments.count()})


# ----------------------------
# 💬 Messaging System
# ----------------------------
@login_required
def inbox(request):
    messages_qs = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-timestamp')

    # Build conversation list containing partner user, last message, and unread count
    conv_map = {}
    for msg in messages_qs:
        partner = msg.receiver if msg.sender == request.user else msg.sender
        if partner.username not in conv_map:
            # unread messages for this partner (where partner is sender and receiver is request.user)
            unread_count = Message.objects.filter(sender=partner, receiver=request.user, is_read=False).count()
            conv_map[partner.username] = {
                'partner': partner,
                'last_msg': msg,
                'unread': unread_count
            }

    # Convert to a list sorted by last_msg timestamp
    conversations = sorted(conv_map.values(), key=lambda x: x['last_msg'].timestamp, reverse=True)
    return render(request, 'blog/inbox.html', {'conversations': conversations})


@login_required
def chat_view(request, username):
    user2 = get_object_or_404(User, username=username)
    messages_qs = Message.objects.filter(
        Q(sender=request.user, receiver=user2) | Q(sender=user2, receiver=request.user)
    ).order_by('timestamp')

    # mark messages as read
    Message.objects.filter(receiver=request.user, sender=user2, is_read=False).update(is_read=True)

    # Build conversation list for sidebar (same structure as inbox view)
    all_msgs = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-timestamp')
    conv_map = {}
    for msg in all_msgs:
        partner = msg.receiver if msg.sender == request.user else msg.sender
        if partner.username not in conv_map:
            unread_count = Message.objects.filter(sender=partner, receiver=request.user, is_read=False).count()
            conv_map[partner.username] = {
                'partner': partner,
                'last_msg': msg,
                'unread': unread_count
            }
    conversations = sorted(conv_map.values(), key=lambda x: x['last_msg'].timestamp, reverse=True)

    # compute last_id for client polling to avoid fetching already-rendered messages
    last_id = messages_qs.last().pk if messages_qs.exists() else 0

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = user2
            msg.save()
            return redirect('chat', username=username)
    else:
        form = MessageForm()

    return render(request, 'blog/chat.html', {
        'user2': user2,
        'messages': messages_qs,
        'form': form,
        'conversations': conversations,
        'last_id': last_id,
    })


@login_required
@require_POST
def send_message_ajax(request, username):
    """AJAX endpoint to send a message to `username`. Returns rendered message HTML."""
    user2 = get_object_or_404(User, username=username)
    body = request.POST.get('body', '').strip()
    if not body:
        return JsonResponse({'error': 'Empty message'}, status=400)
    msg = Message.objects.create(sender=request.user, receiver=user2, body=body, timestamp=timezone.now())
    # Render message partial
    html = render_to_string('blog/_message.html', {'msg': msg, 'request': request})
    return JsonResponse({'success': True, 'message_html': html, 'msg_id': msg.pk})


@login_required
@require_GET
def chat_messages_ajax(request, username):
    """Return rendered HTML for messages in conversation since optional `after` message id."""
    user2 = get_object_or_404(User, username=username)
    after = request.GET.get('after')
    qs = Message.objects.filter(
        Q(sender=request.user, receiver=user2) | Q(sender=user2, receiver=request.user)
    ).order_by('timestamp')
    if after and after.isdigit():
        qs = qs.filter(pk__gt=int(after))
    html = ''
    for msg in qs:
        html += render_to_string('blog/_message.html', {'msg': msg, 'request': request})
    # mark as read the ones sent to request.user
    Message.objects.filter(receiver=request.user, sender=user2, is_read=False).update(is_read=True)
    return JsonResponse({'success': True, 'messages_html': html, 'last_id': qs.last().pk if qs.exists() else None})


@login_required
@require_POST
def toggle_comment_like_ajax(request, pk):
    """Toggle like on a comment via AJAX."""
    from .models import Comment
    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'like_count': comment.likes.count()})
