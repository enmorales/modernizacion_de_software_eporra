import os

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object("apostador.config.Config")
    return app