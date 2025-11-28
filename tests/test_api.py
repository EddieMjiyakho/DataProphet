import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

class TestAPIEndpoints:
    """Test all API endpoints"""
    
    def test_health_check(self, client: TestClient):
        """Test health check endpoint"""
        response = client.get("/health_check")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
    
    def test_ingest_polymers_unauthorized(self, client: TestClient):
        """Test polymer ingestion without authentication"""
        polymer_data = [{
            "timestamp": "2023-07-10T08:00:21.123",
            "polymer": "aBc"
        }]
        
        response = client.post("/polymers", json=polymer_data)
        assert response.status_code == 403
    
    def test_ingest_polymers_success(self, client: TestClient, auth_headers: dict):
        """Test successful polymer ingestion"""
        polymer_data = [{
            "timestamp": "2023-07-10T08:00:21.123",
            "polymer": "aBc"
        }]
        
        response = client.post("/polymers", json=polymer_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert len(data) == 1
        assert data[0]["polymer"] == "aBc"
    
    def test_ingest_polymers_duplicate_timestamp(self, client: TestClient, auth_headers: dict):
        """Test polymer ingestion with duplicate timestamp"""
        polymer_data = [{
            "timestamp": "2023-07-10T08:00:21.123",
            "polymer": "aBc"
        }]
        
        # First request should succeed
        response1 = client.post("/polymers", json=polymer_data, headers=auth_headers)
        assert response1.status_code == 201
        
        # Second request with same timestamp should fail
        response2 = client.post("/polymers", json=polymer_data, headers=auth_headers)
        assert response2.status_code == 409
    
    def test_ingest_polymers_invalid_data(self, client: TestClient, auth_headers: dict):
        """Test polymer ingestion with invalid data"""
        # Polymer too long
        polymer_data = [{
            "timestamp": "2023-07-10T08:00:21.123",
            "polymer": "a" * 129  # 129 characters - too long
        }]
        
        response = client.post("/polymers", json=polymer_data, headers=auth_headers)
        assert response.status_code == 422  # Validation error
    
    def test_get_polymers_success(self, client: TestClient, auth_headers: dict):
        """Test retrieving polymers by time range"""
        # First, ingest some test data
        test_data = [
            {
                "timestamp": "2023-07-10T08:00:00.000",
                "polymer": "abc"
            },
            {
                "timestamp": "2023-07-10T08:01:00.000", 
                "polymer": "def"
            }
        ]
        
        client.post("/polymers", json=test_data, headers=auth_headers)
        
        # Retrieve polymers
        start = "2023-07-10T08:00:00"
        end = "2023-07-10T08:02:00"
        response = client.get(f"/polymers?start={start}&end={end}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "polymers" in data
        assert len(data["polymers"]) == 2
    
    def test_get_polymers_invalid_time_range(self, client: TestClient, auth_headers: dict):
        """Test retrieving polymers with invalid time range"""
        start = "2023-07-10T09:00:00"  # After end
        end = "2023-07-10T08:00:00"    # Before start
        
        response = client.get(f"/polymers?start={start}&end={end}", headers=auth_headers)
        assert response.status_code == 400
    
    def test_reactor_endpoint_success(self, client: TestClient, auth_headers: dict):
        """Test reactor endpoint with sample data"""
        # Ingest polymers that will react
        test_data = [
            {
                "timestamp": "2023-07-10T08:00:00.000",
                "polymer": "aA"
            },
            {
                "timestamp": "2023-07-10T08:01:00.000",
                "polymer": "bB"
            }
        ]
        
        client.post("/polymers", json=test_data, headers=auth_headers)
        
        # Get reactor result
        start = "2023-07-10T08:00:00"
        end = "2023-07-10T08:02:00"
        response = client.get(f"/reactor?start={start}&end={end}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == ""  # All polymers should react to empty string
        assert data["reaction_count"] == 2
    
    def test_reactor_endpoint_no_data(self, client: TestClient, auth_headers: dict):
        """Test reactor endpoint with no polymers in time range"""
        start = "2023-07-10T09:00:00"
        end = "2023-07-10T10:00:00"
        
        response = client.get(f"/reactor?start={start}&end={end}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == ""
        assert data["reaction_count"] == 0

    def test_reactor_complex_reaction(self, client: TestClient, auth_headers: dict):
        """Test reactor with complex polymer reaction"""
        # From assignment example
        test_data = [{
            "timestamp": "2023-07-10T08:00:00.000",
            "polymer": "AaefxxxXB"
        }]
    
        client.post("/polymers", json=test_data, headers=auth_headers)
    
        start = "2023-07-10T08:00:00"
        end = "2023-07-10T08:01:00"
        response = client.get(f"/reactor?start={start}&end={end}", headers=auth_headers)
    
        assert response.status_code == 200
        data = response.json()
        # Our algorithm produces "efxxB" with 2 reactions for this input
        assert data["result"] == "efxxB"
        assert data["reaction_count"] == 2