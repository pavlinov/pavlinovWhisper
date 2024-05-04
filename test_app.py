import os
from quart import url_for
import pytest
from app import app as quart_app

@pytest.fixture
def app():
    yield quart_app

@pytest.fixture
def client(app):
    return app.test_client()

async def test_heartbeat(client):
    response = await client.get('/')
    assert response.status_code == 200
    json = await response.get_json()
    assert json == {"status": "alive", "message": "Server is running"}

async def test_upload_file(client):
    data = {
        'file': (open('test_audio.mp3', 'rb'), 'test_audio.mp3')
    }
    response = await client.post(await url_for('upload_file'), data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    json = await response.get_json()
    assert json['message'] == 'File uploaded successfully'
    assert json['filename'] == 'test_audio.mp3'
    # Check if file is in the folder
    assert os.path.isfile('public/upload/test_audio.mp3')

# Clean up after tests
def teardown_module(module):
    os.remove('public/upload/test_audio.mp3')
