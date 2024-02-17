from fastapi.testclient import TestClient
from app.main import app  # Adjust import based on your project structure

client = TestClient(app)

def test_read_profiles():
    response = client.get("/profiles/")
    assert response.status_code == 200
    assert response.json()  # Assert that some response is returned

def test_read_profile():
    profile_id = 1  # Assuming this ID exists
    response = client.get(f"/profiles/{profile_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == profile_id  # Ensure the response has the correct profile
