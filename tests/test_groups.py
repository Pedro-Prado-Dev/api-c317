import unittest

from app import create_app
from app.config import Config
from app.extensions import db
from app.group.model import Group
from app.users.model import User


class TestGroupResource(unittest.TestCase):
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

    def test_get_all_groups(self):
        response = self.client.get("/groups")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_group(self):
        group_data = {"name": "Test Group", "description": "This is a test group"}
        response = self.client.post("/groups", json=group_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], group_data["name"])

    def test_get_single_group(self):
        group = Group(name="Get Group", description="A group to get")
        db.session.add(group)
        db.session.commit()

        response = self.client.get(f"/groups/{group.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], group.name)

    def test_update_group(self):
        group = Group(name="Update Group", description="Group before update")
        db.session.add(group)
        db.session.commit()

        updated_data = {"name": "Updated Group"}
        response = self.client.put(f"/groups/{group.id}", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], updated_data["name"])

    def test_delete_group(self):
        group = Group(name="Delete Group", description="Group to be deleted")
        db.session.add(group)
        db.session.commit()

        response = self.client.delete(f"/groups/{group.id}")
        self.assertEqual(response.status_code, 204)

    def test_add_user_to_group(self):
        user = User(
            name="User for Group", phone_number="555555555", email="usergroup@example.com", role="user", is_adm=False
        )
        user.set_password("password")
        db.session.add(user)
        group = Group(name="Add User Group", description="Group to add user to")
        db.session.add(group)
        db.session.commit()

        response = self.client.post(f"/groups/{group.id}/users/{user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("User for Group", [u["name"] for u in response.json["users"]])

    def test_remove_user_from_group(self):
        user = User(
            name="Remove User", phone_number="555555555", email="removeuser@example.com", role="user", is_adm=False
        )
        user.set_password("password")
        group = Group(name="Remove User Group", description="Group to remove user from")
        group.users.append(user)
        db.session.add(group)
        db.session.commit()

        response = self.client.delete(f"/groups/{group.id}/users/{user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("User removed from group", response.json["message"])


if __name__ == "__main__":
    unittest.main(exit=False)
