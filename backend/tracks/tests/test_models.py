from django.test import TestCase

from tracks.models import TrackPoint


class ModelsTests(TestCase):
    def test_model_str(self):
        track = TrackPoint.objects.create(
            point_x=50, point_y=50, file_name="track1.csv"
        )
        self.assertEqual(
            str(track), f"{track.point_x}, {track.point_y} ({track.file_name})"
        )
