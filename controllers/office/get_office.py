from controllers.create_app_route import app_route
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request
from models import Department, Employee, Office
from models.database import db
from sqlalchemy.sql import func
import flask
from helper import current_user
import sqlalchemy.exc
import builtins



@app_route.route('/offices', methods=['GET'])
@app_route.route('/offices/', methods=['GET'])
@jwt_required()
def get_offices():
    tokenData = get_jwt_identity()
    country = request.args.get('country')
    current_employee = current_user(tokenData['staff_number'])

    if current_employee['role'] in ['Engineer', 'Head of department']:
        return jsonify({"msg":"No access"}), 403
    else:
        allOffices = Office.query. \
            filter((func.lower(Office.country) == country.lower()) if country else True).all()
        if allOffices == []:
            return jsonify({"msg":"Not found office"}), 400

        output = []
        for office in allOffices:
            if current_employee['role'] == 'Head':
                output.append(office_dict_formation(office))
            elif current_employee['role'] == 'Head of office' and current_employee['office_id'] == office.id:
                output.append(office_dict_formation(office))

        if output:
            return jsonify(output)
        else:
            return jsonify({"msg":"No access"}), 403


@app_route.route('/office/<title>', methods=['GET'])
@jwt_required()
def get_office(title):
    tokenData = get_jwt_identity()
    current_employee = current_user(tokenData['staff_number'])

    if current_employee['role'] in ['Engineer', 'Head of department']:
        return jsonify({"msg":"No access"}), 403
    else:
        try:
            office = Office.query.filter(func.lower(Office.title) == title.lower()).one()
        except sqlalchemy.exc.NoResultFound as message:
            print(message)
            return jsonify({"msg":"Not found office"}), 400

        if office.id == current_employee['office_id']:
            return office_dict_formation(office)
        else:
            return jsonify({"msg":"No access"}), 403


def office_dict_formation(office):
    # Formation of a dictionary of office parameters
    res = {}
    res['id'] = office.id
    res['title'] = office.title
    res['country'] = office.country
    res['address'] = office.address
    res['amount_departments'] = Department.query.filter_by(office_id=office.id).count()
    res['amount_employees'] = Employee.query.join(Department).filter_by(office_id=office.id).count()
    res['payroll_costs'] = db.session.query(func.sum(Employee.salary)).join(Department) \
        .filter_by(office_id=office.id).one()[0]

    return res
