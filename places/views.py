from django.contrib.gis.geos import GEOSGeometry
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
import numpy as np

from places.models import Place
from places.serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        queryset = Place.objects.all()
        coords = self.request.query_params.get("coords")

        if coords:
            x, y = [float(coord.strip()) for coord in coords.split(",")]
            point = GEOSGeometry(f"SRID=4326;POINT({x} {y})")
            places_points = [GEOSGeometry(place.geom) for place in queryset]
            distances = [point.distance(place_point) for place_point in places_points]
            queryset = queryset.filter(geom=places_points[np.argmin(distances)])

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "coords",
                type=str,
                description="Get the nearest place to provided coordinates (ex. ?coords=48.87,2.29)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get a list of places."""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a place."""
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a place by ID."""
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update a place by ID."""
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Update a place partially by ID."""
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete a place by ID."""
        return super().destroy(request, *args, **kwargs)
