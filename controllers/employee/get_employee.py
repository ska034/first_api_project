from flask import jsonify

from controllers.create_app_route import app_route

from models import Employee
from sqlalchemy.sql import func
from models.database import db



@app_route.route('/employees', methods=['GET'])
def get_employee():
    allEmployees = Employee.query.all()
    # res1 = db.session.query(func.sum(Employee.salary)).one()
    # print (res1[0])

    # print(Employee.query.func.sum(Employee.salary).one())

    output = []
    for employee in allEmployees:
        res = {}
        res['id'] = employee.id
        res['last_name'] = employee.last_name
        res['first_name'] = employee.first_name
        res['patronymic'] = employee.patronymic
        res['department_id'] = employee.department_id
        res['role_id'] = employee.role_id
        res['salary'] = employee.salary
        output.append(res)

    return jsonify(output)
