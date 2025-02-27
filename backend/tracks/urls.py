from django.urls import path
from .views import TrackUploadView, TrackPointListView, FileListView

app_name = "tracks"

urlpatterns = [
    path("upload/", TrackUploadView.as_view(), name="file-upload"),
    path("", TrackPointListView.as_view(), name="track-points"),
    path("files/", FileListView.as_view(), name="files"),
]
