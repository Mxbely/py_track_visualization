import dash_leaflet as dl
from dash import Dash, html, dcc
import base64
import io
from dash.dependencies import Input, Output
import requests

app = Dash(__name__, suppress_callback_exceptions=True)


def get_file_list():
    response = requests.get("http://127.0.0.1:8000/api/tracks/files/")
    if response.status_code == 200:
        print("file_list", response.json())
        return response.json()
    return []


def get_track_points(file_name):
    response = requests.get(
        f"http://127.0.0.1:8000/api/tracks/?file_name={file_name}"
    )
    if response.status_code == 200:
        return response.json()
    return []


app.layout = html.Div(
    [
        html.H1("Upload your file"),
        dcc.Upload(
            id="upload-data",
            children=html.Button("Upload File"),
            multiple=False,
        ),
        html.Div(id="output-data"),
        html.Div(id="upload-status"),
        html.Div(id="my-output"),
        dcc.Dropdown(id="file-dropdown", placeholder="Select a file"),
        dl.Map(
            id="map",
            children=[
                dl.TileLayer(),
            ],
            center=[50, 30],
            zoom=6,
            style={"height": "50vh"},
        ),
    ],
)


@app.callback(Output("map", "children"), Input("file-dropdown", "value"))
def update_map(selected_file):
    if not selected_file:
        return [dl.TileLayer()]

    track_points = get_track_points(selected_file)

    if not track_points:
        return [dl.TileLayer()]

    polyline = dl.Polyline(
        positions=[[p["point_x"], p["point_y"]] for p in track_points],
        color="red",
    )

    return [dl.TileLayer(), polyline]


def parse_contents(contents):
    content_type, content_string = contents.split(",")
    print("content_type", content_type)
    print("content_string", content_string)
    decoded = base64.b64decode(content_string)
    return io.BytesIO(decoded)


@app.callback(
    Output("upload-status", "children"),
    Output("file-dropdown", "options", allow_duplicate=True),
    Input("upload-data", "filename"),
    Input("upload-data", "contents"),
    prevent_initial_call='initial_duplicate',
)
def upload_file(filename, contents):
    if not contents or not filename:
        return "", []

    file_io = parse_contents(contents)
    files = {"file": (filename, file_io, "application/csv")}

    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/tracks/upload/", files=files
        )
        dropdown_options = []
        if response.status_code == 201:
            file_list = get_file_list()
            print(file_list)
            dropdown_options = [{"label": f, "value": f} for f in file_list]

            return "File uploaded successfully!", dropdown_options

        elif response.status_code == 409:
            return f"File {filename} already exists", dropdown_options
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        print(f"Request failed: {e}")
        return "Error during upload", dropdown_options


@app.callback(
        Output("file-dropdown", "options", allow_duplicate=True), 
        Input("file-dropdown", "id"),
        prevent_initial_call='initial_duplicate',
    )
def load_existing_files(_):
    file_list = get_file_list()
    return [{"label": f, "value": f} for f in file_list]


if __name__ == "__main__":
    app.run_server(debug=True)
