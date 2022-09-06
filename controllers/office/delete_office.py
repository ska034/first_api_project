from controllers.create_app_route import app_route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper import current_user
from models.database import db
from models import Office
import sqlalchemy.exc
import flask


@app_route.route('/offices', methods=['DELETE'])
@jwt_required()
def del_office():
    tokenData = get_jwt_identity()
    officeData = request.get_json()
    current_employee = current_user(tokenData['staff_number'])

    if current_employee['role'] == 'Head':
        try:
            deleteOffice = Office.query.filter_by(title=officeData['title']).one()
        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return jsonify({"msg":"Not found office"}), 400

        db.session.delete(deleteOffice)
        db.session.commit()

        return jsonify({"msg":"Deleted successfully"}), 200
    else:
        return jsonify({"msg":"No access"}), 403
