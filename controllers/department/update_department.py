from controllers.create_app_route import app_route
from flask import request
from models import Department
from models.database import db
import config  # temporally
import flask
import helper
import sqlalchemy.exc


@app_route.route('/departments', methods=['PATCH'])
def update_department():
    departmentData = request.get_json()
    current_employee = helper.current_user(config.staff_number)  # temporally

    if current_employee['role'] in ['Head', 'Head of office']:
        if current_employee['role'] == 'Head of office' and (
                current_employee['office_id'] != departmentData['office_id'] or current_employee['office_id'] !=
                departmentData['new_office_id']):
            return flask.make_response("You do not have access to update a department in another office.", 403)
        try:
            editedDepartment = Department.query.filter_by(title=departmentData['title']). \
                filter_by(office_id=departmentData['office_id']).one()

        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return flask.make_response("Error. There is no department with this title in this office.", 400)

        alldepartment = Department.query.all()

        for department in alldepartment:
            if departmentData['new_title'] == department.title and departmentData[
                'new_office_id'] == department.office_id:
                return flask.make_response("Error. An department with this title already exists in this office.", 403)

        editedDepartment.title = departmentData['new_title']
        editedDepartment.office_id = departmentData['new_office_id']

        db.session.add(editedDepartment)

        try:
            db.session.flush()
        except sqlalchemy.exc.IntegrityError as message:
            print(message)
            db.session.rollback()
            return flask.make_response("Error. An department with this title already exists in this office.", 403)

        db.session.commit()
        return flask.make_response(
            f"Department '{departmentData['title']}' changed to:\n\n Title: {editedDepartment.title}"
            f"\nOffice_id: {editedDepartment.office_id}", 200)
    else:
        return flask.make_response("You do not have access to these actions.", 403)
