from typing import Any

import dash_leaflet as dl
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from utils import (
    get_all_list_options,
    get_track_points,
    parse_contents,
    update_files,
)

app = Dash(__name__, suppress_callback_exceptions=True)

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
def update_map(selected_file: str) -> list:
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


@app.callback(
    Output("upload-status", "children"),
    Output("file-dropdown", "options", allow_duplicate=True),
    Input("upload-data", "filename"),
    Input("upload-data", "contents"),
    prevent_initial_call="initial_duplicate",
)
def upload_file(filename: str, contents: str) -> tuple:
    if not contents or not filename:
        return "Upload your file", get_all_list_options()

    file_io = parse_contents(contents)
    files = {"file": (filename, file_io, "application/csv")}

    try:
        response = update_files(files)
        dropdown_options = get_all_list_options()

        if response.status_code == 201:
            return "File uploaded successfully!", dropdown_options

        elif response.status_code == 409:
            return f"File {filename} already exists", dropdown_options
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        print(f"Request failed: {e}")
        return "Error during upload", dropdown_options


@app.callback(
    Output("file-dropdown", "options"),
    Input("file-dropdown", "id"),
    prevent_initial_call=True,
)
def load_existing_files(*args: Any) -> list:
    return get_all_list_options()


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
