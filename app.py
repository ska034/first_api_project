from datetime import timedelta
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from controllers import app_route
from controllers.create_jwt_manager import jwt
from models.database import db
from config import db_connection_string, jwt_secret_key

app = Flask(__name__)
client  = app.test_client()

app.config['SQLALCHEMY_DATABASE_URI'] = db_connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)



app.register_blueprint(app_route)
jwt.init_app(app)



db.init_app(app)
migrate = Migrate(app, db)
import models

if __name__ == "__main__":
    app.run(debug=True)
