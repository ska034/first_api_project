from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from controllers.office.office import app_route
from models.database import db
import config

app = Flask(__name__)
app.register_blueprint(app_route)
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

import models

if __name__ == "__main__":
    app.run(debug=True)
