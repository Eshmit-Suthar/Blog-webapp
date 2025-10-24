from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('posts-by-category', kwargs={'slug': self.slug})

def upload_to_post(instance, filename):
    return f'posts/{instance.author.username}/{filename}'

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=upload_to_post, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # auto-generate slug if not set
        if not self.slug:
            base = slugify(self.title)[:200]
            slug_candidate = base
            num = 1
            while Post.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f"{base}-{num}"
                num += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
