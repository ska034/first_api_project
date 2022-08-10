import sqlalchemy.exc
import flask
from flask import request

from controllers.create_app_route import app_route

from models.database import db
from models import Office


@app_route.route('/offices', methods=['DELETE'])
def del_office():
    officeData = request.get_json()
    try:
        deleteOffice = Office.query.filter_by(title=officeData['title']).one()
    except sqlalchemy.exc.NoResultFound:
        return flask.make_response("There is no office with this title.", 400)

    db.session.delete(deleteOffice)
    db.session.commit()

    return flask.make_response("Good deletion", 200)
