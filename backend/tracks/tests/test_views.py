import tempfile
from io import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from tracks.models import TrackPoint

MAIN_URL = "http://django:8000/api/tracks/"
CSV_DATA = "10.0,20.0\n30.0,40.0"


class TrackUploadViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = f"{MAIN_URL}upload/"

    def test_upload_valid_file(self):
        csv_data = CSV_DATA
        file = InMemoryUploadedFile(
            StringIO(csv_data),
            "file",
            "track.csv",
            "text/csv",
            len(csv_data),
            None,
        )

        response = self.client.post(
            self.url, {"file": file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "File data saved")
        self.assertEqual(TrackPoint.objects.count(), 2)

    def test_upload_no_file(self):
        response = self.client.post(self.url, {}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "No file uploaded")

    def test_upload_file_exists(self):
        csv_data = CSV_DATA
        file = InMemoryUploadedFile(
            StringIO(csv_data),
            "file",
            "track.csv",
            "text/csv",
            len(csv_data),
            None,
        )
        self.client.post(self.url, {"file": file}, format="multipart")

        response = self.client.post(
            self.url, {"file": file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.data["error"], "File with this name already exists"
        )


class TrackPointListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = f"{MAIN_URL}"
        self.track_name = "track.csv"

        TrackPoint.objects.create(
            file_name=self.track_name, point_x=10.0, point_y=20.0
        )
        TrackPoint.objects.create(
            file_name=self.track_name, point_x=30.0, point_y=40.0
        )

    def test_get_track_points_by_file_name(self):
        response = self.client.get(self.url, {"file_name": self.track_name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["point_x"], 10.0)
        self.assertEqual(response.data[0]["point_y"], 20.0)

    def test_get_no_track_points(self):
        response = self.client.get(self.url, {"file_name": "nonexistent.csv"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class FileListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = f"{MAIN_URL}files/"

        TrackPoint.objects.create(
            file_name="track1.csv", point_x=10.0, point_y=20.0
        )
        TrackPoint.objects.create(
            file_name="track2.csv", point_x=30.0, point_y=40.0
        )

    def test_get_file_names(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("track1.csv", response.data)
        self.assertIn("track2.csv", response.data)
