import base64
import io

import requests
from rest_framework.response import Response

MAIN_URL = "http://django:8000/api/tracks/"


def get_file_list() -> list:
    response = requests.get(f"{MAIN_URL}files/")
    if response.status_code == 200:
        return response.json()
    return []


def get_track_points(file_name: str) -> list:
    response = requests.get(f"{MAIN_URL}?file_name={file_name}")
    if response.status_code == 200:
        return response.json()
    return []


def get_all_list_options() -> list[dict]:
    file_list = get_file_list()
    return [{"label": f, "value": f} for f in file_list]


def update_files(files: str) -> Response:
    return requests.post(f"{MAIN_URL}upload/", files=files)


def parse_contents(contents: str) -> str:
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    return io.BytesIO(decoded)
