import sqlalchemy.exc
import flask
from flask import jsonify, request

from controllers.create_app_route import app_route

from models.database import db
from models import Office


@app_route.route('/offices', methods=['POST'])
def add_office():
    officeData = request.get_json()

    new_office = Office(title=officeData['title'], country=officeData['country'], address=officeData['address'])
    db.session.add(new_office)

    try:
        db.session.flush()

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return flask.make_response("Error. An office with this name already exists.", 403)

    finally:
        db.session.commit()

    return flask.make_response(jsonify(officeData), 200)
