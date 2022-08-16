import sqlalchemy.exc
import flask
from flask import request

from controllers.create_app_route import app_route

from models.database import db
from models import Department


@app_route.route('/departments', methods=['DELETE'])
def del_department():
    departmentData = request.get_json()

    try:
        deleteDepartment = Department.query.filter_by(title=departmentData['title']). \
            filter_by(office_id=departmentData['office_id']).one()

    except sqlalchemy.exc.NoResultFound as message:
        print(message)
        return flask.make_response("There is no department with this title in office.", 400)

    db.session.delete(deleteDepartment)
    db.session.commit()

    return flask.make_response("Good deletion", 200)
