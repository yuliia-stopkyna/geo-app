from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from places.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    geom = GeometryField()

    class Meta:
        model = Place
        fields = ("id", "name", "description", "geom")
