import sqlalchemy.exc
import flask
from flask import request

from controllers.create_app_route import app_route

from models.database import db
from models import Employee


@app_route.route('/employees', methods=['DELETE'])
def del_employee():
    employeeData = request.get_json()
    try:
        deleteEmployee = Employee.query.filter_by(staff_number=employeeData['staff_number']).one()
    except sqlalchemy.exc.NoResultFound:
        return flask.make_response("There is no employee with this staff number.", 400)

    db.session.delete(deleteEmployee)
    db.session.commit()

    return flask.make_response("Good deletion", 200)
