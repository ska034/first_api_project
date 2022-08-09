import sqlalchemy.exc
import flask
from flask import Blueprint, jsonify, request

app_route = Blueprint('app_route', __name__)
from models.database import db
from models import Office


@app_route.route('/offices', methods=['GET'])
def get_office():
    allOffices = Office.query.all()
    output = []
    for office in allOffices:
        res = {}
        res['title'] = office.title
        res['country'] = office.country
        res['address'] = office.address
        output.append(res)

    return jsonify(output)


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


@app_route.route('/offices', methods=['DELETE'])
def del_office():
    officeData = request.get_json()
    try:
        deleteOffice = Office.query.filter_by(id=officeData['id']).one()
    except sqlalchemy.exc.NoResultFound:
        return flask.make_response("There is no office with this id.", 400)

    db.session.delete(deleteOffice)
    db.session.commit()

    return flask.make_response("Good deletion", 200)
