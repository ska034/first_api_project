from controllers.create_app_route import app_route
from flask import request
from models import Department
from models import Employee
from models.database import db
import config       # temporally
import sqlalchemy.exc
import flask
import helper


@app_route.route('/employees', methods=['PATCH'])
def update_employee():
    employeeData = request.get_json()
    current_employee = helper.current_user(config.staff_number)  # temporally

    if current_employee['role'] in ['Head', 'Head of office']:
        if current_employee['role'] == 'Head of office' and current_employee['office_id'] != employeeData['office_id']:
            return flask.make_response("You do not have access to update a employee in another office.", 403)

        try:
            editedEmployee = Employee.query.filter_by(staff_number=employeeData['staff_number']).one()
        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return flask.make_response("Error. There is no employee with this staff number.", 400)

        try:
           is_department = Department.query.\
               filter(employeeData['department_id'] == Department.id, employeeData['office_id'] == Department.office_id).\
               one()
        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return flask.make_response("There is no such department in this office.", 400)

        if 'new_staff_number' in employeeData.keys() and employeeData['new_staff_number']:
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
        except sqlalchemy.exc.IntegrityError as message:
            print(message)
            db.session.rollback()
            return flask.make_response("Error. An employee with this staff number already exists.", 403)

        db.session.commit()
        return flask.make_response(f"Employee '{employeeData['staff_number']}' changed to:\n"
                                   f"\n Staff number: {editedEmployee.staff_number}\nLast name: {editedEmployee.last_name}"
                                   f"\nFirst name: {editedEmployee.first_name}\nPatronymic: {editedEmployee.patronymic}"
                                   f"\nDepartment id: {editedEmployee.department_id}\nRole id: {editedEmployee.role_id}"
                                   f"\nSalary: {editedEmployee.salary}", 200)
    else:
        return flask.make_response("You do not have access to these actions.", 403)
