from flask import Flask

from .extension import db
from .api import main


def create_app(db_url="sqlite:///users.db"):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SECRET_KEY"] = "FesC9cBSuxakv9yN0vBY"

    db.init_app(app)

    app.register_blueprint(main)

    return app
