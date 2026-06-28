from app import app


def test_hola_mundo():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"Hola Mundo"
