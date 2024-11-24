import pytest
from api import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_get_books(client):
    rv = client.get('/books')
    assert rv.status_code == 200
    response_json = rv.get_json()
    assert 'count' in response_json
    assert 'books' in response_json
