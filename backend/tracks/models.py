from django.db import models


class TrackPoint(models.Model):
    point_x = models.FloatField()
    point_y = models.FloatField()
    file_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.point_x}, {self.point_y} ({self.file_name})"

