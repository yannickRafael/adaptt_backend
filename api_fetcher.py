import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("COST_API_BASE_URL")
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "False").lower() == "true"

def fetch_public_projects():
    """Fetches all public projects from the CoST API."""
    if USE_MOCK_DATA:
        print("Using Mock Data for public projects")
        # Return a simplified mock structure matching the new format
        return [
            {
                "id": "mock1",
                "name": "Mock Project 1",
                "status": "Implementation",
                "documents": []
            }
        ]

    url = f"{BASE_URL}/getPublicProjects"
    try:
        response = requests.get(url, timeout=30) # Increased timeout for bulk data
        response.raise_for_status()
        data = response.json()
        return data.get('projects', [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching public projects: {e}")
        return []

def fetch_locations():
    """Fetches all locations from the API."""
    if USE_MOCK_DATA:
        return [
            {"id": "maputo-city", "name": "Maputo City", "region": "South", "country": "Mozambique"},
            {"id": "gaza", "name": "Gaza", "region": "South", "country": "Mozambique"}
        ]
    
    try:
        url = f"{BASE_URL}/getLocations"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching locations: {e}")
        return []
