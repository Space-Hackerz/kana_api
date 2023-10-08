import os
from pathlib import Path

from flask import Flask
from .api import db
from .rest_api import info
from . import rest_api


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="KANA_IS_THE_CUTEST!!!",
        DATABASE=Path(app.instance_path) / Path("kana_api.sqlite"),
    )

    if not test_config:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(info.info_bp)

    return app
