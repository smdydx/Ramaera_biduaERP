
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "CRM + HRMS API is running" in response.json()["message"]

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_api_status():
    """Test API status endpoint"""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    assert response.json()["api_version"] == "v1"
