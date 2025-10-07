# tracking/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .storage import inspection_store, zone_store


# -------------------------
# HTML Page Views
# -------------------------

def supervisor_dashboard(request):
    """Main supervisor interface for viewing/assigning inspectors."""
    return render(request, "supervisor.html")


def map_designer(request):
    """Map designer for defining zones per airport level."""
    return render(request, "map.html")


# -------------------------
# Inspector APIs
# -------------------------

class InspectionListView(APIView):
    """Returns list of inspectors and their assignments."""

    def get(self, request):
        data = inspection_store.get_all()
        return Response(data, status=status.HTTP_200_OK)


# -------------------------
# Zone APIs
# -------------------------

class ZoneListView(APIView):
    """Returns all zones for a given airport level."""

    def get(self, request):
        level = request.GET.get("level")
        zones = zone_store.get_all_zones(level)
        return Response(zones, status=status.HTTP_200_OK)


class ZoneCreateView(APIView):
    """Create a new zone polygon or circle on a level."""

    def post(self, request):
        name = request.data.get("name")
        coords = request.data.get("coordinates")
        zone_type = request.data.get("type", "polygon")
        level = request.data.get("level", "L1")

        if not name or not coords:
            return Response(
                {"error": "Missing name or coordinates"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        level_zones = zone_store.get_all_zones(level)
        new_id = str(len(level_zones) + 1)

        zone_store.add_zone(
            level,
            new_id,
            {"name": name, "type": zone_type, "coordinates": coords},
        )

        return Response(
            {
                "message": f"Zone '{name}' created on {level}",
                "zone": zone_store.levels[level][new_id],
            },
            status=status.HTTP_201_CREATED,
        )


class ZoneAssignView(APIView):
    """Assigns an inspector to a zone on a specific level."""

    def post(self, request):
        level = request.data.get("level", "L1")
        zone_id = request.data.get("zone_id")
        inspector_id = request.data.get("inspector_id")

        if not zone_id or not inspector_id:
            return Response(
                {"error": "Missing zone_id or inspector_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        success = zone_store.assign_inspector(level, zone_id, inspector_id)
        if success:
            return Response(
                {"message": f"Inspector {inspector_id} assigned to zone {zone_id}"},
                status=status.HTTP_200_OK,
            )
        return Response({"error": "Zone not found"}, status=status.HTTP_404_NOT_FOUND)


class ZoneAssignmentsListView(APIView):
    def get(self, request):
        output = []

        for level, zones in zone_store.levels.items():
            level_assignments = zone_store.get_assignments(level)

            for zone_id, inspector_list in level_assignments.items():
                zone = zones.get(zone_id)
                if not zone:
                    continue

                for inspector_id in inspector_list:
                    output.append({
                        "inspector_id": inspector_id,
                        "level": level,
                        "zone_id": zone_id,
                        "zone_name": zone["name"],
                    })

        return Response(output, status=status.HTTP_200_OK)
