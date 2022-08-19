from controllers.create_app_route import app_route
from flask import request
from models import Department
from models.database import db
import config       # temporally
import flask
import helper
import sqlalchemy.exc


@app_route.route('/departments', methods=['DELETE'])
def del_department():
    departmentData = request.get_json()
    current_employee = helper.current_user(config.staff_number)  # temporally

    if current_employee['role'] in ['Head','Head of office']:
        try:
            deleteDepartment = Department.query.filter_by(title=departmentData['title']). \
                filter_by(office_id=departmentData['office_id']).one()
            if current_employee['role'] == 'Head of office' and current_employee['office_id'] != deleteDepartment.office_id:
                return flask.make_response("You do not have access to these actions.", 403)
        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return flask.make_response("There is no department with this title in office.", 400)

        db.session.delete(deleteDepartment)
        db.session.commit()

        return flask.make_response("Good deletion", 200)
    else:
        return flask.make_response("You do not have access to these actions.", 403)