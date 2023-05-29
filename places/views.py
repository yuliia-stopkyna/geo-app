from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets

from places.models import Place
from places.serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()

    def filter_queryset(self, queryset):
        coords = self.request.query_params.get("coords")

        if coords:
            x, y = [float(coord.strip()) for coord in coords.split(",")]
            point = Point(x, y, srid=4326)
            queryset = queryset.annotate(distance=Distance("geom", point)).order_by("distance")[:1]

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
