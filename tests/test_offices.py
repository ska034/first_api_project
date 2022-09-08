from unittest import TestCase, main
from app import app
from models import Office
from tests.config_test import headers, URL
import requests


class TestOfficeNotToken(TestCase):
    def test_01_get_offices_not_token(self):
        response = requests.get(URL + "/offices")
        self.assertEqual(response.status_code, 401)


class TestOfficeIsTokenHead(TestCase):

    def test_01_get_offices_status_code(self):
        response = requests.get(URL + "/offices", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_02_get_office_value_from_db(self):
        response = requests.get(URL + "/office/head", headers=headers)
        title_from_response = response.json().get('title')
        with app.app_context():
            title_from_db = Office.query.filter(Office.title == 'Head').one().title
        self.assertEqual(title_from_response, title_from_db)

    def test_03_create_office_json_response(self):
        response = requests.post(URL + "/offices", headers=headers,
                                 json={
                                     "title": "Test_office",
                                     "country": "Georgia",
                                     "address": "secret address"
                                 })
        self.assertEqual(response.json().get('msg'), 'Created successfully')

    def test_04_create_office_value_from_db(self):
        with app.app_context():
            data_from_db = Office.query.filter(Office.title == 'Test_office').one()
        office_from_db = dict(title=data_from_db.title, country=data_from_db.country, address=data_from_db.address)
        office_from_requests = {"title": "Test_office", "country": "Georgia", "address": "secret address"}
        self.assertEqual(office_from_requests, office_from_db)

    def test_05_update_office_json_response(self):
        response = requests.patch(URL + "/offices", headers=headers,
                                  json={
                                      "title": "Test_office",
                                      "new_title": "No name office"
                                  })
        self.assertEqual(response.json().get('msg'), 'Changed successfully')

    def test_06_update_office_old_value_from_db(self):
        with app.app_context():
            data_from_db = Office.query.filter(Office.title == 'Test_office').all()
        self.assertEqual(data_from_db,[])

    def test_07_update_office_new_value_from_db(self):
        with app.app_context():
            data_from_db = Office.query.filter(Office.title == 'No name office').one()
        office_from_db = dict(title=data_from_db.title, country=data_from_db.country, address=data_from_db.address)
        office_from_requests = {"title": "No name office", "country": "Georgia", "address": "secret address"}
        self.assertEqual(office_from_requests, office_from_db)

    def test_08_delete_office_json_response(self):
        response = requests.delete(URL + "/offices", headers=headers, json={"title": "No name office"})
        self.assertEqual(response.json().get('msg'), 'Deleted successfully')

    def test_09_delete_office_value_from_db(self):
        with app.app_context():
            data_from_db = Office.query.filter(Office.title == 'No name office').all()
        self.assertEqual(data_from_db, [])

    def test_10_delete_non_existing_office_status_code(self):
        response = requests.delete(URL + "/offices", headers=headers, json={"title": "Test"})
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    main()
