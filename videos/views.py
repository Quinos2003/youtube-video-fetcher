from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from .models import Video
from .serializers import VideoSerializer

class VideoCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-published_at'

class VideoListView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = VideoCursorPagination
