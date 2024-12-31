from django.apps import AppConfig

class VideosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videos'

    def ready(self):
        from .tasks import FetchVideosThread
        fetcher_thread = FetchVideosThread()
        fetcher_thread.setDaemon(True)  # Ensures thread stops when server stops
        fetcher_thread.start()