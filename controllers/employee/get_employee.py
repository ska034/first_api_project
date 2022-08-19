from controllers.create_app_route import app_route
from flask import jsonify, request, redirect, url_for
from models import Department
from models import Employee
from models import Office
from models import Role
from models.database import db
from sqlalchemy.sql import func
import config  # temprally
import flask
import helper
import sqlalchemy.exc


@app_route.route('/employees', methods=['GET'])
@app_route.route('/employees/', methods=['GET'])
def get_employees():
    office = request.args.get('office')
    department = request.args.get('department')
    salary = request.args.get('salary')
    role = request.args.get('role')

    current_employee = helper.current_user(config.staff_number)  # temporally

    if current_employee['role'] == 'Engineer':
        return redirect(url_for('app_route.get_employee', staff_number=current_employee['staff_number']))
    else:
        allEmployees = Employee.query \
            .join(Department) \
            .join(Office) \
            .join(Role) \
            .filter((func.lower(Department.title) == department.lower()) if department else True) \
            .filter((func.lower(Office.title) == office.lower()) if office else True) \
            .filter((Employee.salary == salary) if salary else True) \
            .filter((func.lower(Role.position) == role.lower()) if role else True) \
            .all()
        if allEmployees == []:
            return flask.make_response("There is no employee with the given parameters.", 400)

    output = []
    for employee in allEmployees:
        if current_employee['role'] == "Head":
            output.append(employee_dict_formation(employee))
        else:
            if current_employee['role'] == "Head of office" \
                    and current_employee['office_id'] == employee.department.office_id:
                output.append(employee_dict_formation(employee))
            elif current_employee['role'] == "Head of department" \
                    and current_employee['department_id'] == employee.department_id:
                output.append(employee_dict_formation(employee))
    if output:
        return jsonify(output)
    else:
        return flask.make_response("You do not have access to this information.", 403)


@app_route.route('/employee/<int:staff_number>')
def get_employee(staff_number):
    current_employee = helper.current_user(config.staff_number)  # temporally

    try:
        allemployees = Employee.query.filter_by(staff_number=staff_number).one()
    except sqlalchemy.exc.NoResultFound as message:
        print(message)
        return flask.make_response("There is no employee with the given parameters.", 400)

    if current_employee['role'] == 'Head':
        return employee_dict_formation(allemployees)
    elif current_employee['role'] == 'Head of office' and current_employee['office_id'] == allemployees.department.office_id:
        return employee_dict_formation(allemployees)
    elif current_employee['role'] == 'Head of department' and current_employee['department_id'] == allemployees.department_id:
        return employee_dict_formation(allemployees)
    elif current_employee['role'] == 'Engineer' and current_employee['staff_number'] == allemployees.staff_number:
        return employee_dict_formation(allemployees)
    else:
        return flask.make_response("You do not have access to this information.", 403)


def employee_dict_formation(employee):
    # Formation of a dictionary of employee parameters
    res = {}
    res['id'] = employee.id
    res['last_name'] = employee.last_name
    res['first_name'] = employee.first_name
    res['patronymic'] = employee.patronymic
    res['department_id'] = employee.department_id
    res['role'] = employee.role.position
    res['salary'] = employee.salary
    res['department'] = employee.department.title
    res['office'] = employee.department.office.title

    return res
