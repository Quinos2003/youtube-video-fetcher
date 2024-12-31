from django.contrib import admin

# Register your models here.

from .models import Video, APIKey

admin.site.register(Video)
admin.site.register(APIKey)