from controllers.create_app_route import app_route
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper import current_user
from models import Department
from models.database import db
import flask
import sqlalchemy.exc


@app_route.route('/departments', methods=['POST'])
@jwt_required()
def add_department():
    tokenData = get_jwt_identity()
    departmentData = request.get_json()
    current_employee = current_user(tokenData['staff_number'])

    if current_employee['role'] in ['Head','Head of office']:
        if current_employee['role'] == 'Head of office' and current_employee['office_id'] != departmentData['office_id']:
            return jsonify({"msg":"No access"}), 403
        alldepartment = Department.query.all()
        for department in alldepartment:
            if departmentData['title'] == department.title and departmentData['office_id'] == department.office_id:
                return jsonify({"msg":"Already exists"}), 403

        new_department = Department(title=departmentData['title'], office_id=departmentData['office_id'])
        db.session.add(new_department)

        try:
            db.session.flush()

        except sqlalchemy.exc.IntegrityError as message:
            print(message)
            db.session.rollback()
            return jsonify({"msg":"Already exists"}), 403

        finally:
            db.session.commit()

        return jsonify({"msg":"Created successfully"}), 200
    else:
        return jsonify({"msg":"No access"}), 403