from flask import jsonify

from controllers.create_app_route import app_route

from models.database import db
from models import Department
from models import Office


@app_route.route('/departments', methods=['GET'])
def get_department():
    # alldepartment = Department.query.all()

    alldepartment = Department.query.join(Office,Office.id==Department.office_id).all()

    print(alldepartment)

    output = []
    for department in alldepartment:
        res = {}
        res['id'] = department.id
        res['title'] = department.title
        res['office_id'] = department.office_id
        res['office_title'] = department.office.title
        res['country'] = department.office.country
        output.append(res)

    return jsonify(output)
