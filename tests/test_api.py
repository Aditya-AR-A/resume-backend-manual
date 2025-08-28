import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "status" in data

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_status_endpoint():
    """Test the status endpoint"""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "data" in data

def test_config_endpoint():
    """Test the config endpoint"""
    response = client.get("/api/v1/config")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "data" in data

# Note: Data endpoints would require actual data files to test properly
# These tests serve as a template for when data files are available

def test_ai_status_endpoint():
    """Test the AI status endpoint"""
    response = client.get("/api/v1/ai/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "components" in data
    assert "providers" in data
