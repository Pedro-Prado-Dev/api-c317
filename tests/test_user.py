import unittest
from flask import json
from app import create_app
from app.users.model import User
from app.config import Config
from app.extensions import db

class TestUserResource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(Config)
        cls.app.testing = True
        cls.client = cls.app.test_client()

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.connection = db.engine.connect()
        self.transaction = self.connection.begin()

    def tearDown(self):
        self.transaction.rollback()
        self.connection.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_all_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_user(self):
        user_data = {
            "name": "Test User",
            "phone_number": "123456789",
            "email": "test10@example.com",
            "password": "password",
            "role": "user",
            "is_adm": False
        }
        response = self.client.post('/users', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['email'], user_data['email'])

    def test_get_single_user(self):
        user = User(name="Get User", phone_number="987654321", email="getuser@example.com", role="user", is_adm=False)
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        response = self.client.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], user.email)

    def test_update_user(self):
        user = User(name="Update User", phone_number="555555555", email="updateuser@example.com", role="user", is_adm=False)
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        updated_data = {"name": "Updated Name"}
        response = self.client.put(f'/users/{user.id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], updated_data['name'])

    def test_delete_user(self):
        user = User(name="Delete User", phone_number="333333333", email="deleteuser@example.com", role="user", is_adm=False)
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        response = self.client.delete(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("User deleted", response.json['message'])

if __name__ == "__main__":
    unittest.main(exit=False)
