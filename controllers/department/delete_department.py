from controllers.create_app_route import app_route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper import current_user
from models import Department
from models.database import db
import flask
import sqlalchemy.exc


@app_route.route('/departments', methods=['DELETE'])
@jwt_required()
def del_department():
    tokenData = get_jwt_identity()
    departmentData = request.get_json()
    current_employee = current_user(tokenData['staff_number'])

    if current_employee['role'] in ['Head','Head of office']:
        if current_employee['role'] == 'Head of office' and current_employee['office_id'] != departmentData[
            'office_id']:
            return jsonify({"msg":"No access"}), 403
        try:
            deleteDepartment = Department.query.filter_by(title=departmentData['title']). \
                filter_by(office_id=departmentData['office_id']).one()
            if current_employee['role'] == 'Head of office' and current_employee['office_id'] != deleteDepartment.office_id:
                return jsonify({"msg":"No access"}), 403
        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return jsonify({"msg":"Not found department"}), 400

        db.session.delete(deleteDepartment)
        db.session.commit()

        return jsonify({"msg":"Deleted successfully"}), 200
    else:
        return jsonify({"msg":"No access"}), 403