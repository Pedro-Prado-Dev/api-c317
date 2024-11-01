import unittest

from app import create_app
from app.config import Config
from app.extensions import db
from app.form.model import Form
from app.group.model import Group


class TestFormResource(unittest.TestCase):
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

    def test_get_all_forms(self):
        response = self.client.get("/forms")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_form(self):
        group = Group(name="Test Group", description="This is a test group")
        db.session.add(group)
        db.session.commit()

        form_data = {
            "title": "Test Form",
            "color": "#FFFFFF",
            "image": "test.png",
            "group": group.id,
            "components": [{"type": "multiple", "title": "Sample Component", "options": ["Option 1", "Option 2"]}],
        }
        response = self.client.post("/forms", json=form_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["title"], form_data["title"])

    def test_get_single_form(self):
        group = Group(name="Test Group", description="This is a test group")
        db.session.add(group)
        db.session.commit()

        form = Form(title="Test Form", color="#FFFFFF", image="test.png", group_id=group.id)
        db.session.add(form)
        db.session.commit()

        response = self.client.get(f"/forms/{form.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["title"], form.title)

    def test_update_form(self):
        group = Group(name="Test Group", description="This is a test group")
        db.session.add(group)
        db.session.commit()

        form = Form(title="Old Form", color="#FFFFFF", image="old.png", group_id=group.id)
        db.session.add(form)
        db.session.commit()

        updated_data = {"title": "Updated Form"}
        response = self.client.put(f"/forms/{form.id}", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["title"], updated_data["title"])

    def test_delete_form(self):
        group = Group(name="Test Group", description="This is a test group")
        db.session.add(group)
        db.session.commit()

        form = Form(title="Delete Form", color="#FFFFFF", image="delete.png", group_id=group.id)
        db.session.add(form)
        db.session.commit()

        response = self.client.delete(f"/forms/{form.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Form deleted", response.json["message"])


if __name__ == "__main__":
    unittest.main(exit=False)
