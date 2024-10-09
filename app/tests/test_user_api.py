import unittest
from app.users.model import User
from app.tests.base_test import BaseTestCase



class TestUserResource(BaseTestCase):

    def test_get_users(self):
        """Testando GET na rota /users"""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)

    def test_get_user(self):
        """Testando GET na rota /users/<id>"""
        user = User.query.first()
        response = self.client.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], user.name)

    def test_get_user_not_found(self):
        """Testando GET na rota /users/<id> para um ID que não existe"""
        response = self.client.get('/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.json['error'])
    def test_post_user(self):
        """Testando POST na rota /users"""
        user_data = {
            'name': 'John Doe',
            'phone_number': '987654321',
            'email': 'john@example.com',
            'password': '123456',
            'role': 'admin'
        }
        response = self.client.post('/users', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('John Doe', response.json['name'])

    def test_post_user_missing_data(self):
        """Testando POST na rota /users com dados faltando"""
        user_data = {
            'name': 'John Doe',
            'phone_number': '987654321',
            'email': 'john@example.com',
        }
        response = self.client.post('/users', json=user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing data", response.json['error'])

    def test_post_user_email_already_exists(self):
        """Testando POST na rota /users com email já existente"""
        user_data = {
            'name': 'Test User',
            'phone_number': '123456789',
            'email': 'test@example.com',
            'password': 'newpassword',
            'role': 'user'
        }
        response = self.client.post('/users', json=user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email already in use", response.json['error'])

    def test_put_user(self):
        """Testando PUT na rota /users/<id>"""
        user = User.query.first()
        update_data = {
            'name': 'Updated Name',
            'phone_number': '123456789',
            'email': 'updated@example.com',
            'role': 'admin'
        }
        response = self.client.put(f'/users/{user.id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated Name')

    def test_put_user_not_found(self):
        """Testando PUT na rota /users/<id> para um ID que não existe"""
        update_data = {
            'name': 'Nonexistent User'
        }
        response = self.client.put('/users/999', json=update_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.json['error'])

    def test_delete_user(self):
        """Testando DELETE na rota /users/<id>"""
        user = User.query.first()
        response = self.client.delete(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("User deleted", response.json['message'])

    def test_delete_user_not_found(self):
        """Testando DELETE na rota /users/<id> para um ID que não existe"""
        response = self.client.delete('/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.json['error'])

if __name__ == '__main__':
    unittest.main()
