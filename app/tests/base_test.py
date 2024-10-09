from flask_testing import TestCase
from app import create_app, db
from app.users.model import User


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # banco de dados em memória
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        """Setup before each test."""
        db.create_all()
        self.create_test_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_test_user(self):
        user = User(
            name="Test User",
            phone_number="123456789",
            email="test@example.com",
            role="user",
            is_adm=False
        )
        user.set_password("password")
        db.session.add(user)
        db.session.commit()