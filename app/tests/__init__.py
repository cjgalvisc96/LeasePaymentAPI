import unittest

from app import create_app, db


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app(settings_module="config.testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
