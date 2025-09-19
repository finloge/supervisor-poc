"""
URL configuration for SupervisorPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tracking.views import (
    UpdateLocationView,
    ListLocationsView,
    map_view,
    InspectionListView,
    InspectionUpdateLocationView,
    GeofenceListView,
    InspectorAssignmentView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/update-location/", UpdateLocationView.as_view(), name="update_location"),
    path("api/locations/", ListLocationsView.as_view(), name="locations"),
    path("api/inspections/", InspectionListView.as_view(), name="inspections"),
    path("api/geofences/", GeofenceListView.as_view(), name="geofences"),
    path("api/inspection-update/", InspectionUpdateLocationView.as_view(), name="inspection_update"),
    path("api/assignment/<str:inspector_id>/", InspectorAssignmentView.as_view()),
    path("dashboard/", map_view, name="map"),
]

