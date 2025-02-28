import csv
from io import TextIOWrapper

from drf_spectacular.utils import (
    OpenApiParameter, 
    OpenApiResponse,
    extend_schema
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import TrackPoint
from .serializers import TrackPointSerializer


class TrackUploadView(APIView):
    @extend_schema(
        description="Upload CSV file with track points",
        request={"data": {"file": "binary"}},
        responses={
            201: OpenApiResponse(description="File data saved"),
            400: OpenApiResponse(description="No file uploaded"),
            409: OpenApiResponse(
                description="File with this name already exists"
            ),
        },
    )
    def post(self, request: Request) -> Response:
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        existing_file = TrackPoint.objects.filter(file_name=file.name)
        if existing_file:
            return Response(
                {"error": "File with this name already exists"}, status=409
            )

        track_name = file.name

        decoded_file = TextIOWrapper(file, encoding="utf-8")
        csv_reader = csv.reader(decoded_file)
        points = []
        for row in csv_reader:
            try:
                points.append(
                    TrackPoint(
                        file_name=track_name,
                        point_x=float(row[0]),
                        point_y=float(row[1]),
                    )
                )
            except (ValueError, IndexError):
                continue

        TrackPoint.objects.bulk_create(points)

        return Response(
            {"message": "File data saved"}, status=201
        )


class TrackPointListView(APIView):
    @extend_schema(
        description="Recive track points by file name",
        parameters=[
            OpenApiParameter(
                name="file_name",
                description="Name of the file with track points",
                required=True,
                type=str,
            )
        ],
        responses={
            200: TrackPointSerializer(many=True),
        },
    )
    def get(self, request: Request) -> Response:
        file_name = request.query_params.get("file_name")
        track_points = TrackPoint.objects.filter(file_name=file_name)
        serializer = TrackPointSerializer(track_points, many=True)
        return Response(serializer.data, status=200)


class FileListView(APIView):
    @extend_schema(
        description="Recive list of unique file names from db",
        responses={
            200: OpenApiResponse(description="List of file names"),
        },
    )
    def get(self, request: Request) -> Response:
        file_names = TrackPoint.objects.values_list(
            "file_name", flat=True
        ).distinct()
        return Response(file_names, status=200)
