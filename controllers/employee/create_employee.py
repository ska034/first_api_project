import sqlalchemy.exc
import flask
from flask import jsonify, request

from controllers.create_app_route import app_route

from models.database import db
from models import Employee


@app_route.route('/employees', methods=['POST'])
def add_employee():
    employeeData = request.get_json()

    if 'patronymic' not in employeeData:
        employeeData['patronymic'] = ''

    new_employee = Employee(last_name=employeeData['last_name'], first_name=employeeData['first_name'],
                            patronymic=employeeData['patronymic'], department_id=employeeData['department_id'],
                            role_id=employeeData['role_id'], salary=employeeData['salary'], staff_number=employeeData['staff_number'])
    db.session.add(new_employee)

    try:
        db.session.flush()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()

        return flask.make_response("Error. An employee with this staff number already exists.", 403)

    finally:
        db.session.commit()

    return flask.make_response(jsonify(employeeData), 200)
