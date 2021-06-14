import pytest

from flask_augmentations.app import app


IMAGE_URL = "https://cdn.pixabay.com/photo/2021/04/29/11/40/big-ben-6216420_960_720.jpg"


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_app__ok(client):
    r = client.get(f"/?url={IMAGE_URL}")
    assert r.status_code == 200, r.status_code
    assert b'<img src="/static/augmented_image.jpg"' in r.data, r.data
