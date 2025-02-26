from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import TrackPoint
from io import TextIOWrapper
import csv


class TrackUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({'error': 'No file uploaded'}, status=400)

        track_name = file.name

        decoded_file = TextIOWrapper(file, encoding='utf-8')
        csv_reader = csv.reader(decoded_file)
        print(csv_reader)
        points = []
        for row in csv_reader:
            try:

                points.append(TrackPoint(
                    file_name=track_name,
                    point_x=float(row[0]),
                    point_y=float(row[1])
                ))
            except (ValueError, IndexError):
                continue

        TrackPoint.objects.bulk_create(points)

        return Response({'message': 'File processed and data saved'}, status=201)
