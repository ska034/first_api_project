import flask
from flask import jsonify, request
from controllers.create_app_route import app_route
from models import Department
from models import Employee
from models import Office
from models.database import db
from sqlalchemy.sql import func


@app_route.route('/offices', methods=['GET'])
@app_route.route('/offices/', methods=['GET'])
def get_offices():
    country = request.args.get('country')
    if country:
        allOffices = Office.query.filter_by(country=country).all()
    else:
        allOffices = Office.query.all()

    output = []
    for office in allOffices:
        output.append(office_dict_formation(office))
    if output:
        return jsonify(output)
    else:
        return flask.make_response("There are no offices in this country", 400)


@app_route.route('/office/<title>', methods=['GET'])
def get_office(title):
    office = Office.query.filter_by(title=title).one()

    return office_dict_formation(office)


def office_dict_formation(office):
    # Formation of a dictionary of office parameters
    res = {}
    res['id'] = office.id
    res['title'] = office.title
    res['country'] = office.country
    res['address'] = office.address
    res['amount_departments'] = Department.query.filter_by(office_id=office.id).count()
    res['amount_employees'] = Employee.query.join(Department, Department.id == Employee.department_id). \
        filter_by(office_id=office.id).count()
    res['payroll_costs'] = db.session.query(db.func.sum(Employee.salary)).join(Department, Department.id == Employee.department_id). \
        filter_by(office_id=office.id).one()[0]

    return res
