from .models import BlogSetting


def blog_settings(request):
    """Add the first BlogSetting instance to templates as `blog_setting`.

    Admins can manage BlogSetting via Django admin.
    """
    setting = None
    try:
        setting = BlogSetting.objects.first()
    except Exception:
        setting = None
    return {'blog_setting': setting}
