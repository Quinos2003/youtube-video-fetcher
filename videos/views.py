from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from .models import Video
from .serializers import VideoSerializer

# add pagination via video_id field
class VideoListPagination(PageNumberPagination):
    page_size = 10

class VideoListView(ListAPIView):
    queryset = Video.objects.all().order_by('-published_at')
    serializer_class = VideoSerializer
    pagination_class = VideoListPagination
