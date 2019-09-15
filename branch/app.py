import os
import logging
from flask import Flask
from branch.database import db
from branch.views import branch


def init_logger():
    logging.basicConfig(filename='error.log', level=logging.DEBUG)


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    init_logger()
    app.register_blueprint(branch, url_prefix='')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
