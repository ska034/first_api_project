import helper
from controllers.create_app_route import app_route
from flask import request
from models.database import db
from models import Office
import config
import sqlalchemy.exc
import flask


@app_route.route('/offices', methods=['DELETE'])
def del_office():
    officeData = request.get_json()
    current_employee = helper.current_user(config.staff_number)  # temporally

    if current_employee['role'] == 'Head':
        try:
            deleteOffice = Office.query.filter_by(title=officeData['title']).one()
        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return flask.make_response("There is no office with this title.", 400)

        db.session.delete(deleteOffice)
        db.session.commit()

        return flask.make_response("Good deletion", 200)
    else:
        return flask.make_response("You do not have access to these actions.", 403)
