# tracking/storage.py
from typing import Dict, Any
from threading import Lock


# -------------------------
# Inspector / Assignment Store
# -------------------------
class InspectionStore:
    """Stores inspector task data for supervisor dashboard."""

    def __init__(self):
        self._lock = Lock()
        self.inspections: Dict[str, Dict[str, Any]] = {
            "1": {"title": "Check Warehouse", "lat": None, "lng": None, "radius": 100},
            "2": {"title": "Inspect Office", "lat": None, "lng": None, "radius": 150},
            "3": {"title": "Visit Site A", "lat": None, "lng": None, "radius": 200},
        }

    def get_all(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return self.inspections

    def update_location(self, inspection_id: str, lat: float, lng: float) -> bool:
        """Update an inspector's assigned zone center."""
        with self._lock:
            if inspection_id in self.inspections:
                self.inspections[inspection_id]["lat"] = lat
                self.inspections[inspection_id]["lng"] = lng
                return True
            return False


inspection_store = InspectionStore()


# -------------------------
# Zone Management Store
# -------------------------
class ZoneStore:
    def __init__(self):
        # structure: { level_name: { zone_id: {...zone_data...} } }
        self.levels = {}
        # assignments: { level_name: { zone_id: [inspector_ids...] } }
        self.assignments = {}

    def add_zone(self, level, zone_id, zone_data):
        if level not in self.levels:
            self.levels[level] = {}
        self.levels[level][zone_id] = zone_data

    def get_all_zones(self, level=None):
        if level:
            return self.levels.get(level, {})
        return self.levels

    def assign_inspector(self, level, zone_id, inspector_id):
        """Allow multiple inspectors per zone."""
        if level not in self.levels or zone_id not in self.levels[level]:
            return False
        if level not in self.assignments:
            self.assignments[level] = {}
        if zone_id not in self.assignments[level]:
            self.assignments[level][zone_id] = []
        if inspector_id not in self.assignments[level][zone_id]:
            self.assignments[level][zone_id].append(inspector_id)
        return True

    def get_assignments(self, level=None):
        if level:
            return self.assignments.get(level, {})
        return self.assignments
    
zone_store = ZoneStore()