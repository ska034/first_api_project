from controllers.create_app_route import app_route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper import current_user
from models.database import db
from models import Office
import flask
import sqlalchemy.exc


@app_route.route('/offices', methods=['PATCH'])
@jwt_required()
def update_office():
    tokenData = get_jwt_identity()
    officeData = request.get_json()
    current_employee = current_user(tokenData['staff_number'])

    if current_employee['role'] == 'Head':
        try:
            editedOffice = Office.query.filter_by(title=officeData['title']).one()
        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return jsonify({"msg":"Not found office"}), 400

        if 'new_title' in officeData:
            editedOffice.title = officeData['new_title']
        if 'country' in officeData:
            editedOffice.country = officeData['country']
        if 'address' in officeData:
            editedOffice.address = officeData['address']

        db.session.add(editedOffice)

        try:
            db.session.flush()
        except sqlalchemy.exc.IntegrityError as message:
            print(message)
            db.session.rollback()
            return jsonify({"msg":"Already exists"}), 403

        db.session.commit()
        return jsonify({"msg": "Changed successfully"}), 200
    else:
        return jsonify({"msg":"No access"}), 403
