from controllers.create_app_route import app_route
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper import current_user
from models.database import db
from models import Department, Employee
import flask
import sqlalchemy.exc


@app_route.route('/employees', methods=['POST'])
@jwt_required()
def add_employee():
    tokenData = get_jwt_identity()
    employeeData = request.get_json()
    current_employee = current_user(tokenData['staff_number'])

    if current_employee['role'] in ['Head','Head of office']:
        if current_employee['role'] == 'Head of office' and current_employee['office_id'] != employeeData['office_id']:
            return jsonify({"msg":"No access"}), 403
        try:
           is_department = Department.query.\
               filter(employeeData['department_id'] == Department.id, employeeData['office_id'] == Department.office_id).\
               one()
        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return jsonify({"msg":"Wrong department or office"}), 400


        if 'patronymic' not in employeeData:
            employeeData['patronymic'] = ''

        new_employee = Employee(last_name=employeeData['last_name'], first_name=employeeData['first_name'],
                                patronymic=employeeData['patronymic'], department_id=employeeData['department_id'],
                                role_id=employeeData['role_id'], salary=employeeData['salary'],
                                staff_number=employeeData['staff_number'])
        db.session.add(new_employee)

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