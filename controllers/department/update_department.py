import sqlalchemy.exc
import flask
from flask import request

from controllers.create_app_route import app_route

from models.database import db
from models import Department


@app_route.route('/departments', methods=['PATCH'])
def update_department():
    departmentData = request.get_json()

    try:
        editedDepartment = Department.query.filter_by(title=departmentData['title']). \
            filter_by(office_id=departmentData['office_id']).one()

    except sqlalchemy.exc.NoResultFound as message:
        print(message)
        return flask.make_response("Error. There is no department with this title in this office.", 400)

    alldepartment = Department.query.all()

    for department in alldepartment:
        if departmentData['new_title'] == department.title and departmentData['new_office_id'] == department.office_id:
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
    return flask.make_response(f"Department '{departmentData['title']}' changed to:\n\n Title: {editedDepartment.title}"
                               f"\nOffice_id: {editedDepartment.office_id}", 200)
