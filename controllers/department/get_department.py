import sqlalchemy.exc

from controllers.create_app_route import app_route
from flask import jsonify, request
from models.database import db
from models import Department
from models import Office
from models import Employee
from sqlalchemy.sql import func
import flask
import helper
import config  # temporally


@app_route.route('/departments', methods=['GET'])
@app_route.route('/departments/', methods=['GET'])
def get_departments():
    country = request.args.get('country')
    office_title = request.args.get('office_title')

    current_employee = helper.current_user(config.staff_number)  # temporally

    if current_employee['role'] == 'Engineer':
        return flask.make_response("You do not have access to this information.", 403)
    else:
        alldepartments = Department.query.join(Office) \
            .filter((func.lower(Office.country) == country.lower()) if country else True) \
            .filter((func.lower(Office.title) == office_title.lower()) if office_title else True) \
            .all()
        if alldepartments == []:
            return flask.make_response("There are no departments in this country or this office", 400)

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
            return flask.make_response("You do not have access to this information.", 403)


#
@app_route.route('/department/<title>', methods=['GET'])
def get_department(title):
    current_employee = helper.current_user(config.staff_number)  # temporally

    if current_employee['role'] == 'Engineer':
        return flask.make_response("You do not have access to this information.", 403)
    else:
        alldepartments = Department.query.filter(func.lower(Department.title) == title.lower()).all()

        if alldepartments == 0:
            return flask.make_response("There is no department with this title.", 400)
        elif len(alldepartments) == 1:
            if current_employee['office_id'] == alldepartments[0].office_id \
                    or current_employee['department_id'] == alldepartments[0].id:
                return department_dict_formation(alldepartments[0])
            elif current_employee['role'] == 'Head':
                return department_dict_formation(alldepartments[0])
            else:
                return flask.make_response("You do not have access to this information.", 403)
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
                return flask.make_response("You do not have access to this information.", 403)


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
