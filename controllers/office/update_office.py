import sqlalchemy.exc
import flask
from flask import Blueprint, jsonify, request

from controllers.office.create_app_route import app_route

from models.database import db
from models import Office


@app_route.route('/offices', methods=['PATСH'])
def update_office():
    officeData = request.get_json()

    try:
        editedOffice = Office.query.filter_by(id=officeData['id']).one()
    except sqlalchemy.exc.NoResultFound:
        return flask.make_response("Error. There is no office with this id.", 400)

    editedOffice.title = officeData['title']
    editedOffice.country = officeData['country']
    editedOffice.address = officeData['address']
    db.session.add(editedOffice)

    try:
        db.session.flush()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return flask.make_response("Error. An office with this title already exists.", 403)

    db.session.commit()
    return flask.make_response(f"Office #{editedOffice.id} changed to:\n Title: {editedOffice.title}"
                               f"\nCountry: {editedOffice.country}\nAddress: {editedOffice.address}", 200)
