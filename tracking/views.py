from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .storage import location_store, inspection_store, geofence_store, zone_store
from django.shortcuts import render


class UpdateLocationView(APIView):
    def post(self, request):
        inspector_id = request.data.get("inspector_id")
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        # Validation
        if not inspector_id or latitude is None or longitude is None:
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lat = float(latitude)
            lon = float(longitude)
        except ValueError:
            return Response({"error": "Invalid coordinates"}, status=status.HTTP_400_BAD_REQUEST)

        # Save in memory
        location_store.update_location(inspector_id, lat, lon)
        return Response({"message": "Location updated"}, status=status.HTTP_200_OK)


class ListLocationsView(APIView):
    def get(self, request):
        return Response(location_store.get_all_locations(), status=status.HTTP_200_OK)
    
class InspectionListView(APIView):
    def get(self, request):
        return Response(inspection_store.get_all(), status=status.HTTP_200_OK)
    
class InspectionUpdateLocationView(APIView):
    def post(self, request):
        inspection_id = request.data.get("inspection_id")
        lat = request.data.get("latitude")
        lng = request.data.get("longitude")
        radius = request.data.get("radius", 100)  # default 100m

        if not inspection_id or lat is None or lng is None:
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lat = float(lat)
            lng = float(lng)
            radius = int(radius)
        except ValueError:
            return Response({"error": "Invalid coordinates"}, status=status.HTTP_400_BAD_REQUEST)

        success = inspection_store.update_location(inspection_id, lat, lng)
        if success:
            inspection_store.inspections[inspection_id]["radius"] = radius
            return Response({"message": "Inspection updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Inspection not found"}, status=status.HTTP_404_NOT_FOUND)

class GeofenceListView(APIView):
    def get(self, request):
        return Response(geofence_store.get_all(), status=status.HTTP_200_OK)
    
class InspectorAssignmentView(APIView):
    def get(self, request, inspector_id):
        data = inspection_store.inspections.get(inspector_id)
        if not data:
            return Response({"error": "Inspector not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data, status=status.HTTP_200_OK)

def map_view(request):
    return render(request, "supervisor.html")

class ZoneListView(APIView):
    def get(self, request):
        return Response(zone_store.get_all_zones(), status=status.HTTP_200_OK)
    
class ZoneCreateView(APIView):
    def post(self, request):
        name = request.data.get("name")
        coords = request.data.get("coordinates")

        if not name or not coords:
            return Response({"error": "Missing name or coordinates"}, status=status.HTTP_400_BAD_REQUEST)

        new_id = str(len(zone_store.zones) + 1)
        zone_store.zones[new_id] = {
            "name": name,
            "type": "polygon",
            "coordinates": coords,
        }

        return Response({"message": "Zone saved", "zone": zone_store.zones[new_id]}, status=status.HTTP_201_CREATED)
    
def map_designer(request):
    return render(request, "map.html")

class ZoneAssignmentsListView(APIView):
    def get(self, request):
        assignments = zone_store.get_assignments()
        detailed = {}
        for zone_id, inspector_id in assignments.items():
            zone = zone_store.zones.get(zone_id)
            if zone:
                detailed[inspector_id] = zone["name"]
        return Response(detailed, status=status.HTTP_200_OK)
    
class ZoneAssignView(APIView):
    def post(self, request):
        zone_id = request.data.get("zone_id")
        inspector_id = request.data.get("inspector_id")

        if not zone_id or not inspector_id:
            return Response({"error": "Missing zone_id or inspector_id"}, status=status.HTTP_400_BAD_REQUEST)

        success = zone_store.assign_inspector(zone_id, inspector_id)
        if success:
            return Response({"message": "Inspector assigned successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Zone not found"}, status=status.HTTP_404_NOT_FOUND)