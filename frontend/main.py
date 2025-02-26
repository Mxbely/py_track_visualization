import dash
from dash import html, dcc
import base64
import io
from dash.dependencies import Input, Output
import requests

app = dash.Dash(__name__, suppress_callback_exceptions=True)

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
    ]
)


def parse_contents(contents):
    content_type, content_string = contents.split(",")
    print("content_type", content_type)
    print("content_string", content_string)
    decoded = base64.b64decode(content_string)
    return io.BytesIO(decoded)


@app.callback(
    Output("upload-status", "children"),
    Input("upload-data", "filename"),
    Input("upload-data", "contents"),
    prevent_initial_call=True
)
def upload_file(filename, contents):
    if contents is None:
        return "No file uploaded"

    file_io = parse_contents(contents)
    files = {"file": (filename, file_io, "application/csv")}

    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/tracks/upload/", files=files
        )
        
        if response.status_code == 201:
            return "File uploaded successfully!"
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        print(f"Request failed: {e}")
        return "Error during upload"


if __name__ == "__main__":
    app.run_server(debug=True)
