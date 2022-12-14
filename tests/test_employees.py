from unittest import TestCase, main
from app import app
from models import Employee, Department
from tests.config_test import headers, URL
import requests


class TestEmployeeNotToken(TestCase):
    def test_01_get_employee_not_token(self):
        response = requests.get(URL + "/employees")
        self.assertEqual(response.status_code, 401)


class TestEmployeeIsTokenHead(TestCase):

    def test_01_get_employee_status_code(self):
        response = requests.get(URL + "/employees", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_02_get_employee_value_from_db(self):
        response = requests.get(URL + "/employee/1001", headers=headers)
        employee_from_response = response.json().get('last_name')
        with app.app_context():
            employee_from_db = Employee.query.filter(Employee.staff_number == '1001').first().last_name
        self.assertEqual(employee_from_response, employee_from_db)

    def test_03_create_employee_json_response(self):
        response = requests.post(URL + "/employees", headers=headers,
                                 json={
                                     "staff_number": 1534,
                                     "last_name": "Morozov",
                                     "first_name": "Den",
                                     "department_id": 5,
                                     "office_id": 2,
                                     "role_id": 3,
                                     "salary": 3056
                                 })
        self.assertEqual(response.json().get('msg'), 'Created successfully')

    def test_04_create_employee_value_from_db(self):
        with app.app_context():
            data_from_db = Employee.query.filter(Employee.staff_number == 1534).one()
        employee_from_db = dict(staff_number=data_from_db.staff_number,
                              last_name=data_from_db.last_name,
                              first_name=data_from_db.first_name,
                              department_id=data_from_db.department_id,
                              role_id=data_from_db.role_id,
                              salary=data_from_db.salary)
        employee_from_requests = {"staff_number": 1534, "last_name": "Morozov", "first_name": "Den", "department_id": 5,
                                "role_id": 3, "salary": 3056}
        self.assertEqual(employee_from_requests, employee_from_db)

    def test_05_update_employee_json_response(self):
        response = requests.patch(URL + "/employees", headers=headers,
                                  json={
                                      "staff_number": 1534,
                                      "last_name": "Morozov",
                                      "first_name": "Den",
                                      "department_id": 5,
                                      "office_id": 2,
                                      "role_id": 3,
                                      "salary": 2985
                                  })
        self.assertEqual(response.json().get('msg'), 'Changed successfully')

    def test_06_update_employee_value_from_db(self):
        with app.app_context():
            data_from_db = Employee.query.filter(Employee.staff_number == 1534).one()
        employee_from_db = dict(staff_number=data_from_db.staff_number,
                              last_name=data_from_db.last_name,
                              first_name=data_from_db.first_name,
                              department_id=data_from_db.department_id,
                              role_id=data_from_db.role_id,
                              salary=data_from_db.salary)
        employee_from_requests = {"staff_number": 1534, "last_name": "Morozov", "first_name": "Den", "department_id": 5,
                                "role_id": 3, "salary": 2985}
        self.assertEqual(employee_from_requests, employee_from_db)

    def test_07_delete_employee_json_response(self):
        response = requests.delete(URL + "/employees", headers=headers, json={"staff_number": 1534})
        self.assertEqual(response.json().get('msg'), 'Deleted successfully')

    def test_08_delete_employee_value_from_db(self):
        with app.app_context():
            data_from_db = Employee.query.filter(Employee.staff_number == 1534).all()
        self.assertEqual(data_from_db, [])

    def test_09_delete_non_existing_employee_status_code(self):
        response = requests.delete(URL + "/employees", headers=headers, json={"staff_number": 9999})
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    main()
