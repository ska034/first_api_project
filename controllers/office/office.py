from flask import Blueprint, jsonify, request

app_route = Blueprint('app_route', __name__)
from app import db
from models import Office


@app_route.route('/offices', methods=['GET'])
def get_offices():
    allOffices = Office.query.all()
    output = []
    for office in allOffices:
        res = {}
        res['title'] = office.title
        res['country'] = office.country
        res['address'] = office.address
        output.append(res)

    return jsonify(output)


@app_route.route('/offices', methods=['PUT'])
def added_offices():
    officeData = request.get_json()
    new_office = Office(title=officeData['title'], country=officeData['country'], address=officeData['address'])
    db.session.add(new_office)
    db.session.commit()

    return jsonify(officeData)
