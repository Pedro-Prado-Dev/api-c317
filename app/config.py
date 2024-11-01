import os
import sys

from dotenv import load_dotenv

load_dotenv()
BASEDIR = os.path.dirname(os.path.abspath("../main.py"))
URL_API = os.getenv("URL_API", "sqlite:///:memory:")
STATIC_FOLDER = os.path.join(sys._MEIPASS, "static") if getattr(sys, "frozen", False) else "static"
TEMPLATE_FOLDER = os.path.join(sys._MEIPASS, "templates") if getattr(sys, "frozen", False) else "templates"


class Config:
    FLASK_DEBUG = 1
    SESSION_TYPE = "filesystem"
    SECRET_KEY = "k\x8d-\xbd\xb9\x05\xeax\x92\xd9{H\xf0\x9c\xf9\xde\x91\xc6\xe6\xa8\x14\xf9\x89t"
    SQLALCHEMY_DATABASE_URI = URL_API
    SQLALCHEMY_TRACK_MODIFICATIONS = False
