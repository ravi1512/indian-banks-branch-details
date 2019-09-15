import os
import logging
from flask import Flask
# from database import db
from flask_sqlalchemy import SQLAlchemy
from views import branch

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
db = SQLAlchemy(app)
logging.basicConfig(filename='error.log', level=logging.DEBUG)
app.register_blueprint(branch, url_prefix='')


if __name__ == '__main__':
    app.run()
