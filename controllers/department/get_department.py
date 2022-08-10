from flask import jsonify

from controllers.create_app_route import app_route

from models import Department


@app_route.route('/departments', methods=['GET'])
def get_department():
    alldepartment = Department.query.all()

    output = []
    for department in alldepartment:
        res = {}
        res['id'] = department.id
        res['title'] = department.title
        res['office_id'] = department.office_id
        output.append(res)

    return jsonify(output)
