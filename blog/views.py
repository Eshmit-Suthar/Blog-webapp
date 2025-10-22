from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all().order_by('-date_created')
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'blog/post_detail.html', {'post': post})
