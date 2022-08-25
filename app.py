from datetime import timedelta
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from controllers import app_route
from controllers.create_jwt_maneger import jwt
from models.database import db
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = config.jwt_secret_key


app.register_blueprint(app_route)
jwt.init_app(app)

db.init_app(app)
migrate = Migrate(app, db)
import models

if __name__ == "__main__":
    app.run(debug=True)
