from controllers.create_app_route import app_route
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper import current_user
from models.database import db
from models import Department, Employee, Office
from sqlalchemy.sql import func
import flask


@app_route.route('/departments', methods=['GET'])
@app_route.route('/departments/', methods=['GET'])
@jwt_required()
def get_departments():
    tokenData = get_jwt_identity()
    country = request.args.get('country')
    office_title = request.args.get('office_title')

    current_employee = current_user(tokenData['staff_number'])

    if current_employee['role'] == 'Engineer':
        return jsonify({"msg":"No access"}), 403
    else:
        alldepartments = Department.query.join(Office) \
            .filter((func.lower(Office.country) == country.lower()) if country else True) \
            .filter((func.lower(Office.title) == office_title.lower()) if office_title else True) \
            .all()
        if alldepartments == []:
            return jsonify({"msg":"Not found department"}), 400

        output = []
        for department in alldepartments:
            if current_employee['role'] == "Head":
                output.append(department_dict_formation(department))
            else:
                if current_employee['role'] == 'Head of department' \
                        and current_employee['department_id'] == department.id:
                    output.append(department_dict_formation(department))
                elif current_employee['role'] == 'Head of office' \
                        and current_employee['office_id'] == department.office_id:
                    output.append(department_dict_formation(department))

        if output:
            return jsonify(output)
        else:
            return jsonify({"msg":"No access"}), 403


#
@app_route.route('/department/<title>', methods=['GET'])
@jwt_required()
def get_department(title):
    tokenData = get_jwt_identity()
    current_employee = current_user(tokenData['staff_number'])

    if current_employee['role'] == 'Engineer':
        return jsonify({"msg":"No access"}), 403
    else:
        alldepartments = Department.query.filter(func.lower(Department.title) == title.lower()).all()

        if alldepartments == 0:
            return jsonify({"msg":"Not found department"}), 400
        elif len(alldepartments) == 1:
            if current_employee['office_id'] == alldepartments[0].office_id \
                    or current_employee['department_id'] == alldepartments[0].id:
                return department_dict_formation(alldepartments[0])
            elif current_employee['role'] == 'Head':
                return department_dict_formation(alldepartments[0])
            else:
                return jsonify({"msg":"No access"}), 403
        else:
            output = []
            for department in alldepartments:
                if current_employee['role'] == "Head":
                    output.append(department_dict_formation(department))
                else:
                    if current_employee['role'] == 'Head of department' and current_employee[
                        'department_id'] == department.id:
                        output.append(department_dict_formation(department))
                    elif current_employee['role'] == 'Head of office' and current_employee[
                        'office_id'] == department.office_id:
                        output.append(department_dict_formation(department))

            if output:
                return jsonify(output)
            else:
                return jsonify({"msg":"No access"}), 403


def department_dict_formation(department):
    # Formation of a dictionary of department parameters
    res = {}
    res['id'] = department.id
    res['title'] = department.title
    res['office_id'] = department.office_id
    res['office_title'] = department.office.title
    res['country'] = department.office.country
    res['amount_employees'] = Employee.query.filter_by(department_id=department.id).count()
    res['payroll_costs'] = db.session.query(func.sum(Employee.salary)).filter_by(department_id=department.id).one()[0]

    return res
