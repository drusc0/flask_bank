from scratchfi import create_app, db
from config import TestConfig
import pytest

from scratchfi.models import AccountModel


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_db():
    # Create the database and the database table
    db.create_all()

    # Insert account data
    account = AccountModel(account_num="account_test", balance=20.0, frozen=False)
    db.session.add(account)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()
