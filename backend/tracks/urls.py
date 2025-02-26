from django.urls import path
from .views import TrackUploadView

app_name = "tracks"

urlpatterns = [
    path("upload/", TrackUploadView.as_view(), name="file-upload"),
]
