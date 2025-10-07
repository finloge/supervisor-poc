from django.urls import path
from .views import (
    supervisor_dashboard,
    map_designer,
    InspectionListView,
    ZoneListView,
    ZoneCreateView,
    ZoneAssignView,
    ZoneAssignmentsListView,
)

urlpatterns = [
    path("supervisor/", supervisor_dashboard, name="supervisor-dashboard"),
    path("map-designer/", map_designer, name="map-designer"),

    # APIs
    path("api/inspections/", InspectionListView.as_view(), name="inspections"),
    path("api/zones/", ZoneListView.as_view(), name="zones"),
    path("api/zones/create/", ZoneCreateView.as_view(), name="zone-create"),
    path("api/zone-assign/", ZoneAssignView.as_view(), name="zone-assign"),
    path("api/zone-assignments/", ZoneAssignmentsListView.as_view(), name="zone-assignments"),
]
