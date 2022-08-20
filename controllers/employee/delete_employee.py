from controllers.create_app_route import app_route
from flask import request
from models import Department
from models import Employee
from models.database import db
import config  # temporally
import flask
import sqlalchemy.exc
import helper


@app_route.route('/employees', methods=['DELETE'])
def del_employee():
    employeeData = request.get_json()
    current_employee = helper.current_user(config.staff_number)  # temporally

    if current_employee['role'] in ['Head', 'Head of office']:
        try:
            deleteEmployee = Employee.query.join(Department).filter(Employee.staff_number == employeeData['staff_number'])\
                .one()
            if current_employee['role'] == 'Head of office' and \
                    current_employee['office_id'] != deleteEmployee.department.office_id:
                return flask.make_response("You do not have access to delete a employee in another office.", 403)

        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return flask.make_response("There is no employee with this staff number.", 400)

        db.session.delete(deleteEmployee)
        db.session.commit()

        return flask.make_response("Good deletion", 200)
    else:
        return flask.make_response("You do not have access to these actions.", 403)
