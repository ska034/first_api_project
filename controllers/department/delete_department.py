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
        deleteDepartment = Department.query.filter_by(title=departmentData['title']).one()
    except sqlalchemy.exc.NoResultFound:
        return flask.make_response("There is no department with this title.", 400)

    db.session.delete(deleteDepartment)
    db.session.commit()

    return flask.make_response("Good deletion", 200)
