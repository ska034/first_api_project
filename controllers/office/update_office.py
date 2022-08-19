from controllers.create_app_route import app_route
from flask import request
from models.database import db
from models import Office
import config
import flask
import helper
import sqlalchemy.exc


@app_route.route('/offices', methods=['PATCH'])
def update_office():
    officeData = request.get_json()
    current_employee = helper.current_user(config.staff_number)  # temporally

    if current_employee['role'] == 'Head':
        try:
            editedOffice = Office.query.filter_by(title=officeData['title']).one()
        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return flask.make_response("Error. There is no office with this title.", 400)

        if officeData['new_title']:
            editedOffice.title = officeData['new_title']
        editedOffice.country = officeData['country']
        editedOffice.address = officeData['address']
        db.session.add(editedOffice)

        try:
            db.session.flush()
        except sqlalchemy.exc.IntegrityError as message:
            print(message)
            db.session.rollback()
            return flask.make_response("Error. An office with this title already exists.", 403)

        db.session.commit()
        return flask.make_response(f"Office '{officeData['title']}' changed to:\n\n Title: {editedOffice.title}"
                                   f"\nCountry: {editedOffice.country}\nAddress: {editedOffice.address}", 200)
    else:
        return flask.make_response("You do not have access to these actions.", 403)
