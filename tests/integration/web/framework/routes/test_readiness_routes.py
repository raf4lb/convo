from src.web.http_types import StatusCodes


def test_readiness_endpoint(client):
    # Act
    response = client.get("/ready")

    # Assert
    assert response.status_code == StatusCodes.OK.value
    assert response.json() == {"status": "ready"}
