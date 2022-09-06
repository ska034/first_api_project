from controllers.create_app_route import app_route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper import current_user
from models import Department, Employee
from models.database import db
import sqlalchemy.exc
import flask


@app_route.route('/employees', methods=['PATCH'])
@jwt_required()
def update_employee():
    tokenData = get_jwt_identity()
    employeeData = request.get_json()
    current_employee = current_user(tokenData['staff_number'])

    if current_employee['role'] in ['Head', 'Head of office']:
        if current_employee['role'] == 'Head of office' and current_employee['office_id'] != employeeData['office_id']:
            return jsonify({"msg": "No access"}), 403

        try:
            editedEmployee = Employee.query.filter_by(staff_number=employeeData['staff_number']).one()
        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return jsonify({"msg": "Not found employee"}), 400

        try:
            is_department = Department.query. \
                filter(employeeData['department_id'] == Department.id,
                       employeeData['office_id'] == Department.office_id). \
                one()
        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return jsonify({"msg": "Wrong department or office"}), 400

        if 'new_staff_number' in employeeData and employeeData['new_staff_number']:
            editedEmployee.staff_number = employeeData['new_staff_number']
        if 'last_name' in employeeData:
            editedEmployee.last_name = employeeData['last_name']
        if 'first_name' in employeeData:
            editedEmployee.first_name = employeeData['first_name']
        if 'patronymic' in employeeData:
            editedEmployee.patronymic = employeeData['patronymic']
        if 'department_id' in employeeData:
            editedEmployee.department_id = employeeData['department_id']
        if 'role_id' in employeeData:
            editedEmployee.role_id = employeeData['role_id']
        if 'salary' in employeeData:
            editedEmployee.salary = employeeData['salary']
        db.session.add(editedEmployee)

        try:
            db.session.flush()
        except sqlalchemy.exc.IntegrityError as message:
            print(message)
            db.session.rollback()
            return jsonify({"msg": "Already exists"}), 403

        db.session.commit()
        return jsonify({"msg": "Changed successfully"}), 200
    else:
        return jsonify({"msg": "No access"}), 403
