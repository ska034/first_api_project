from controllers.create_app_route import app_route
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper import current_user
from models.database import db
from models import Office
import flask
import sqlalchemy.exc

@app_route.route('/offices', methods=['POST'])
@jwt_required()
def add_office():
    tokenData = get_jwt_identity()
    officeData = request.get_json()
    current_employee = current_user(tokenData['staff_number'])

    if current_employee['role'] == 'Head':
        new_office = Office(title=officeData['title'], country=officeData['country'], address=officeData['address'])
        db.session.add(new_office)

        try:
            db.session.flush()

        except sqlalchemy.exc.IntegrityError as message:
            print(message)
            db.session.rollback()
            return flask.make_response("Error. An office with this title already exists.", 403)

        finally:
            db.session.commit()

        return flask.make_response(jsonify(officeData), 200)
    else:
        return flask.make_response("You do not have access to these actions.", 403)
