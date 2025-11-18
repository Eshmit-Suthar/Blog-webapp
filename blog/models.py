from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

try:
    from ckeditor.fields import RichTextField
except Exception:
    RichTextField = None

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField() if RichTextField else models.TextField()
    tags = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    # Per-post background options: a solid color or an optional background image
    background_color = models.CharField(max_length=7, blank=True, default='#ffffff')
    background_image = models.ImageField(upload_to='post_backgrounds/', blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following')
    def __str__(self):
        return f"{self.user.username}'s Profile"


class BlogSetting(models.Model):
    """Singleton model to store global blog appearance settings editable via admin."""
    background_color = models.CharField(max_length=7, blank=True, default='#ffffff')
    background_image = models.ImageField(upload_to='site_backgrounds/', blank=True, null=True)

    def __str__(self):
        return "Blog Settings"

    class Meta:
        verbose_name = 'Blog Setting'
        verbose_name_plural = 'Blog Settings'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Exception:
            Profile.objects.get_or_create(user=instance)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=True, default='')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'

