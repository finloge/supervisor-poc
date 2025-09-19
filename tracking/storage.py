from typing import Dict, Any
from threading import Lock

class LocationStore:
    def __init__(self):
        self.data: Dict[str, Dict[str, Any]] = {}
        self.lock = Lock()

    def update_location(self, inspector_id: str, latitude: float, longitude: float):
        with self.lock:
            self.data[inspector_id] = {
                "latitude": latitude,
                "longitude": longitude,
                "last_update": "now"
            }

    def get_all_locations(self):
        with self.lock:
            return self.data

location_store = LocationStore()

class InspectionStore:
    def __init__(self):
        self.inspections = {
            "1": {"title": "Check Warehouse", "lat": None, "lng": None, "radius": 100},
            "2": {"title": "Inspect Office", "lat": None, "lng": None, "radius": 150},
            "3": {"title": "Visit Site A", "lat": None, "lng": None, "radius": 200},
        }

    def get_all(self):
        return self.inspections

    def update_location(self, inspection_id: str, lat: float, lng: float):
        if inspection_id in self.inspections:
            self.inspections[inspection_id]["lat"] = lat
            self.inspections[inspection_id]["lng"] = lng
            return True
        return False

inspection_store = InspectionStore()

class GeofenceStore:
    def __init__(self):
        # Example dummy geofences
        self.geofences = {
            "1": {"name": "Gate A Circle", "type": "circle", "lat": 25.2535, "lng": 55.3650, "radius": 100},
            "2": {"name": "Runway Zone", "type": "polygon", "coords": [
                {"lat": 25.2530, "lng": 55.3645},
                {"lat": 25.2538, "lng": 55.3645},
                {"lat": 25.2538, "lng": 55.3660},
                {"lat": 25.2530, "lng": 55.3660}
            ]}
        }

    def get_all(self):
        return self.geofences

geofence_store = GeofenceStore()
