import flask
import sqlalchemy.exc
from models.database import db
from controllers.create_app_route import app_route
from flask import request
from models import Account
import bcrypt


@app_route.route('/recovery/password', methods=['POST'])
def recovery_password():
    recoveryData = request.get_json()
    try:
        newPassUsers = Account.query.filter_by(login=recoveryData['login']).first()
    except sqlalchemy.exc.NoResultFound as message:
        print(message)
        return flask.make_response("This login not found. Contact the admin.", 400)

    new_password = recoveryData['new_pass'].encode('utf-8')

    newPassUsers.password = str(bcrypt.hashpw(new_password, bcrypt.gensalt()))[2:-1]

    db.session.add(newPassUsers)
    try:
        db.session.flush()
    except Exception as message:
        print(message)
        db.session.rollback()
        return flask.make_response("Error adding data to DB.", 501)
    db.session.commit()

    return "Password changed correctly.", 200


@app_route.route('/login', methods=['POST'])
def login():
    try:
        login = request.json.get('login')
        password = request.json.get('pass')
        if not login:
            return 'Missing login', 400
        if not password:
            return 'Missing password', 400

        login_employee = Account.query.filter_by(login=login).first()

        if not login_employee:
            return 'This login not found', 400

        if bcrypt.checkpw(password.encode('utf-8'), bytes(login_employee.password.encode('utf-8'))):
            return f"Logged in, Welcome {login}", 200
        else:
            return 'Password entered incorrectly', 400

    except AttributeError as message:
        print(message)
        return 'Provide an login and password in JSON format in the request body', 400
