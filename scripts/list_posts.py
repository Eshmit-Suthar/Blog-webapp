import os
import sys
sys.path.append(r'D:\Python\Blog-webapp')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','blogproject.settings')
import django
django.setup()
from blog.models import Post
for p in Post.objects.all():
    print(f"{p.pk}\t{p.title}\tauthor={p.author.username}\tpublished={p.published}\tdate={p.date_posted}")
