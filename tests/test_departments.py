from unittest import TestCase, main
from app import app
from models import Department
from config import headers
import requests

URL = "http://127.0.0.1:5000"


class TestDepartmentNotToken(TestCase):
    def test_01_get_department_not_token(self):
        response = requests.get(URL + "/departments")
        self.assertEqual(response.status_code, 401)


class TestDepartmentIsTokenHead(TestCase):

    def test_01_get_department_status_code(self):
        response = requests.get(URL + "/departments", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_02_get_department_value_from_db(self):
        response = requests.get(URL + "/department/marketing", headers=headers)
        title_from_response = response.json().get('title')
        with app.app_context():
            title_from_db = Department.query.filter(Department.title == 'Marketing').first().title
        self.assertEqual(title_from_response, title_from_db)

    def test_03_post_department_json_response(self):
        response = requests.post(URL + "/departments", headers=headers,
                                 json={
                                     "title": "Test department",
                                     "office_id": 2
                                 })
        self.assertEqual(response.json().get('msg'), 'Created successfully')

    def test_04_patch_department_json_response(self):
        response = requests.patch(URL + "/departments", headers=headers,
                                  json={
                                      "title": "Test department",
                                      "new_title": "No name department",
                                      "office_id": 2,
                                      "new_office_id": 1
                                  })
        self.assertEqual(response.json().get('msg'), 'Changed successfully')

    def test_05_delete_department_json_response(self):
        response = requests.delete(URL + "/departments", headers=headers, json={"title": "No name department",
                                                                                "office_id":1})
        self.assertEqual(response.json().get('msg'), 'Deleted successfully')

    def test_06_delete_non_existing_department_status_code(self):
        response = requests.delete(URL + "/departments", headers=headers, json={"title": "Test",
                                                                                "office_id":3})
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    main()
