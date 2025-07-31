
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    """
    Handle the root URL route.

    Returns:
        str: HTML content displaying a greeting message.
    """
    return "<p>Hello, World!</p>"
