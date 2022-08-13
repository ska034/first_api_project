import sqlalchemy.exc
import flask
from flask import request

from controllers.create_app_route import app_route

from models.database import db
from models import Employee


@app_route.route('/employees', methods=['PATCH'])
def update_employee():
    employeeData = request.get_json()

    try:
        editedEmployee = Employee.query.filter_by(staff_number=employeeData['staff_number']).one()
    except sqlalchemy.exc.NoResultFound as massage:
        print(massage)
        return flask.make_response("Error. There is no employee with this staff number.", 400)

    if employeeData['new_staff_number']:
        editedEmployee.staff_number = employeeData['new_staff_number']
    editedEmployee.last_name = employeeData['last_name']
    editedEmployee.first_name = employeeData['first_name']
    editedEmployee.patronymic = employeeData['patronymic']
    editedEmployee.department_id = employeeData['department_id']
    editedEmployee.role_id = employeeData['role_id']
    editedEmployee.salary = employeeData['salary']
    db.session.add(editedEmployee)

    try:
        db.session.flush()
    except sqlalchemy.exc.IntegrityError as massage:
        print(massage)
        db.session.rollback()
        return flask.make_response("Error. An employee with this staff number already exists.", 403)

    db.session.commit()
    return flask.make_response(f"Employee '{employeeData['staff_number']}' changed to:\n"
                               f"\n Staff number: {editedEmployee.staff_number}\nLast name: {editedEmployee.last_name}"
                               f"\nFirst name: {editedEmployee.first_name}\nPatronymic: {editedEmployee.patronymic}"
                               f"\nDepartment id: {editedEmployee.department_id}\nRole id: {editedEmployee.role_id}"
                               f"\nSalary: {editedEmployee.salary}", 200)
