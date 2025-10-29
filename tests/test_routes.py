import pytest
from app import app

# Skapa testklient
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Testa startsidan
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Personal Finance Dashboard" in response.data

# Testa 404-sida
def test_404(client):
    response = client.get('/icke-existerande-sida')
    assert response.status_code == 404
    assert b"Sidan hittades inte" in response.data
