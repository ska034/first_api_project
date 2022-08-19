from controllers.create_app_route import app_route
from flask import jsonify, request
from models import Department
from models.database import db
import config               # temporally
import flask
import helper
import sqlalchemy.exc


@app_route.route('/departments', methods=['POST'])
def add_department():
    departmentData = request.get_json()
    current_employee = helper.current_user(config.staff_number)  # temporally

    if current_employee['role'] in ['Head','Head of office']:
        alldepartment = Department.query.all()
        for department in alldepartment:
            if departmentData['title'] == department.title and departmentData['office_id'] == department.office_id:
                return flask.make_response("Error. An department with this title already exists in this office.", 403)

        new_department = Department(title=departmentData['title'], office_id=departmentData['office_id'])
        db.session.add(new_department)

        try:
            db.session.flush()

        except sqlalchemy.exc.IntegrityError as message:
            print(message)
            db.session.rollback()
            return flask.make_response("Error. An department with this title already exists in this office.", 403)

        finally:
            db.session.commit()

        return flask.make_response(jsonify(departmentData), 200)
    else:
        return flask.make_response("You do not have access to these actions.", 403)
