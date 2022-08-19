from controllers.create_app_route import app_route
from flask import jsonify, request
from models.database import db
from models import Office
import config
import flask
import helper
import sqlalchemy.exc

@app_route.route('/offices', methods=['POST'])
def add_office():
    officeData = request.get_json()
    current_employee = helper.current_user(config.staff_number)  # temporally

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
