from django.contrib import admin
from .models import Post, Category, Comment, Profile, Message, BlogSetting

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'published')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'content', 'category', 'tags', 'image')
        }),
        ('Publication', {
            'fields': ('published', 'date_posted')
        }),
        ('Appearance', {
            'fields': ('background_color', 'background_image')
        }),
    )

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(BlogSetting)


