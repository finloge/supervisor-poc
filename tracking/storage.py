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
            
        }

    def get_all(self):
        return self.geofences

geofence_store = GeofenceStore()

class ZoneStore:
    def __init__(self):
        self.zones = {}
        self.assignments = {}  # { zone_id: inspector_id }

    def get_all_zones(self):
        return self.zones

    def add_zone(self, zone_id, zone_data):
        self.zones[zone_id] = zone_data

    def assign_inspector(self, zone_id, inspector_id):
        if zone_id in self.zones:
            self.assignments[zone_id] = inspector_id
            return True
        return False

    def get_assignments(self):
        return self.assignments


zone_store = ZoneStore()
