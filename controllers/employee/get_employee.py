from flask import jsonify

from controllers.create_app_route import app_route

from models import Employee


@app_route.route('/employees', methods=['GET'])
def get_employee():
    allEmployees = Employee.query.all()
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
