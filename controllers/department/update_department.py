from controllers.create_app_route import app_route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper import current_user
from models import Department
from models.database import db
import flask
import sqlalchemy.exc


@app_route.route('/departments', methods=['PATCH'])
@jwt_required()
def update_department():
    tokenData = get_jwt_identity()
    departmentData = request.get_json()
    current_employee = current_user(tokenData['staff_number'])

    if current_employee['role'] in ['Head', 'Head of office']:
        if current_employee['role'] == 'Head of office' and (
                current_employee['office_id'] != departmentData['office_id'] or current_employee['office_id'] !=
                departmentData['new_office_id']):
            return jsonify({"msg":"No access"}), 403
        try:
            editedDepartment = Department.query.filter_by(title=departmentData['title']). \
                filter_by(office_id=departmentData['office_id']).one()

        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return jsonify({"msg":"Not found department"}), 400

        alldepartment = Department.query.all()

        for department in alldepartment:
            if departmentData['new_title'] == department.title and departmentData[
                'new_office_id'] == department.office_id:
                return jsonify({"msg": "Already exists"}), 403

        editedDepartment.title = departmentData['new_title']
        editedDepartment.office_id = departmentData['new_office_id']

        db.session.add(editedDepartment)

        try:
            db.session.flush()
        except sqlalchemy.exc.IntegrityError as message:
            print(message)
            db.session.rollback()
            return jsonify({"msg":"Already exists"}), 403

        db.session.commit()
        return jsonify({"msg":"Changed successfully"}), 200
    else:
        return jsonify({"msg":"No access"}), 403
