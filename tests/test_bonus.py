import pytest
from datetime import datetime
from fastapi.testclient import TestClient

class TestBonusFeatures:
    """Test the bonus search filter features"""
    
    def test_polymers_search_length_filters(self, client: TestClient, auth_headers: dict):
        """Test polymer retrieval with length filters"""
        # Create test data with different lengths
        test_data = [
            {
                "timestamp": "2023-07-10T08:00:00.000",
                "polymer": "abc"  # length 3
            },
            {
                "timestamp": "2023-07-10T08:01:00.000",
                "polymer": "abcdef"  # length 6
            },
            {
                "timestamp": "2023-07-10T08:02:00.000", 
                "polymer": "abcdefghi"  # length 9
            }
        ]
        
        client.post("/polymers", json=test_data, headers=auth_headers)
        
        # Test length_gt filter
        response = client.get(
            "/polymers?start=2023-07-10T08:00:00&end=2023-07-10T09:00:00&length_gt=5",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["polymers"]) == 2  # Should get lengths 6 and 9
        
        # Test length_lt filter
        response = client.get(
            "/polymers?start=2023-07-10T08:00:00&end=2023-07-10T09:00:00&length_lt=6",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["polymers"]) == 1  # Should get length 3 only
        
        # Test both filters
        response = client.get(
            "/polymers?start=2023-07-10T08:00:00&end=2023-07-10T09:00:00&length_gt=3&length_lt=9",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["polymers"]) == 1  # Should get length 6 only


    def test_polymers_search_substring_filter(self, client: TestClient, auth_headers: dict):
        """Test polymer retrieval with substring filter (case-insensitive)"""
        test_data = [
            {
                "timestamp": "2023-07-10T08:00:00.000",
                "polymer": "helloWorld"
            },
            {
                "timestamp": "2023-07-10T08:01:00.000",
                "polymer": "worldPeace" 
            },
            {
                "timestamp": "2023-07-10T08:02:00.000",
                "polymer": "goodbyeWorld"
            }
        ]
    
        client.post("/polymers", json=test_data, headers=auth_headers)
    
        # Test substring filter (case-insensitive - should match all)
        response = client.get(
            "/polymers?start=2023-07-10T08:00:00&end=2023-07-10T09:00:00&substring=world",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["polymers"]) == 3  # Should get all three (case-insensitive)
    
        # Test different case (should also match all)
        response = client.get(
            "/polymers?start=2023-07-10T08:00:00&end=2023-07-10T09:00:00&substring=WORLD",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["polymers"]) == 3  # Should get all three (case-insensitive)    
    
    def test_polymers_search_invalid_length_filters(self, client: TestClient, auth_headers: dict):
        """Test polymer retrieval with invalid length filters"""
        response = client.get(
            "/polymers?start=2023-07-10T08:00:00&end=2023-07-10T09:00:00&length_gt=10&length_lt=5",
            headers=auth_headers
        )
        assert response.status_code == 400  # Should fail validation