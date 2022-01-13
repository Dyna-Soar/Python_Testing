import pytest
from flask import Flask,render_template,request,redirect,flash,url_for, session

import os
import tempfile

#from flaskr import create_app
#from flaskr.db import init_db

#@pytest.fixture
def client():
    # fd stands for file descriptor
    db_fd, db_path = tempfile.mkstemp()
    #app = create_app({'TESTING': True, 'DATABASE': db_path})
    app = Flask(__name__)
    app.config.from_pyfile({'TESTING': True, 'DATABASE': db_path})

    #with app.test_client() as client:
    #    with app.app_context():
    #        init_db()
    #    yield client

    os.close(db_fd)
    os.unlink(db_path)

    return tempfile.mkstemp()


print(tempfile.mkstemp())