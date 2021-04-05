from api import create_app

import pytest


@pytest.fixture()
def test_app():
    app = create_app()
    with app.test_client() as test_app:
        with app.app_context():
            yield test_app
