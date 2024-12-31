from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    published_at = models.DateTimeField(db_index=True)
    thumbnail_url = models.URLField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class APIKey(models.Model):
    key = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return self.key
