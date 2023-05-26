from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from places.models import Place
from places.serializers import PlaceSerializer

PLACES_URL = reverse("places:place-list")
PLACE_URL = reverse("places:place-detail", args=[1])


class PlaceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Place.objects.create(
            name="Eiffel Tower",
            description="Wrought-iron lattice tower on the Champ de Mars in Paris, France.",
            geom=GEOSGeometry("SRID=4326;POINT(48.858093 2.294694)"),
        )
        Place.objects.create(
            name="Statue of Liberty",
            description="Sculpture on Liberty Island in New York Harbor in New York City, in the United States.",
            geom=GEOSGeometry("SRID=4326;POINT(40.689247 -74.044502)"),
        )

    def setUp(self) -> None:
        self.client = APIClient()

    def test_places_list(self):
        response = self.client.get(PLACES_URL)
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_place(self):
        data = {
            "name": "Test place",
            "description": "Place description",
            "geom": {"type": "Point", "coordinates": [48.2222, 2.6665]},
        }
        response = self.client.post(PLACES_URL, data=data, format="json")
        new_place = Place.objects.filter(name=data["name"])
        serializer = PlaceSerializer(new_place[0])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(new_place), 1)
        self.assertEqual(serializer.data, response.data)

    def test_retrieve_place(self):
        response = self.client.get(PLACE_URL)
        place = Place.objects.get(id=1)
        serializer = PlaceSerializer(place)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_place(self):
        data = {
            "name": "Test place",
            "description": "Place description",
            "geom": {"type": "Point", "coordinates": [48.2222, 2.6665]},
        }
        response = self.client.put(PLACE_URL, data=data, format="json")
        place = Place.objects.get(id=1)
        serializer = PlaceSerializer(place)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(place.name, data["name"])

    def test_partial_update_place(self):
        data = {"description": "New description"}
        response = self.client.patch(PLACE_URL, data=data, format="json")
        place = Place.objects.get(id=1)
        serializer = PlaceSerializer(place)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(place.description, data["description"])

    def test_delete_place(self):
        response = self.client.delete(PLACE_URL)
        place = Place.objects.filter(id=1)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(place), 0)

    def test_nearest_coordinates_place(self):
        response = self.client.get(PLACES_URL + "?coords=40.742694,-74.171806")
        nearest_place = Place.objects.filter(name="Statue of Liberty")
        serializer = PlaceSerializer(nearest_place, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
