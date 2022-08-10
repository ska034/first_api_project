from flask import Blueprint, jsonify

from controllers.office.create_app_route import app_route

from models import Office


@app_route.route('/offices', methods=['GET'])
def get_office():
    allOffices = Office.query.all()
    output = []
    for office in allOffices:
        res = {}
        res['title'] = office.title
        res['country'] = office.country
        res['address'] = office.address
        output.append(res)

    return jsonify(output)
