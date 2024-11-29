from django.core.management.base import BaseCommand
from property.models import Location
from django.contrib.gis.geos import Point

class Command(BaseCommand):
    help = 'Populates initial location data'

    def handle(self, *args, **options):
        # Example data
        data = [
            {
                "id": "continent_1",
                "title": "North America",
                "center": Point(-100.0, 40.0),
                "location_type": "continent",
                "country_code": "",
                "state_abbr": "",
                "city": "",
            },
            {
                "id": "country_1",
                "title": "United States",
                "center": Point(-95.7129, 37.0902),
                "location_type": "country",
                "country_code": "US",
                "state_abbr": "",
                "city": "",
                "parent_id": "continent_1",
            },
            {
                "id": "state_1",
                "title": "California",
                "center": Point(-119.4179, 36.7783),
                "location_type": "state",
                "country_code": "US",
                "state_abbr": "CA",
                "city": "",
                "parent_id": "country_1",
            },
            {
                "id": "city_1",
                "title": "San Francisco",
                "center": Point(-122.4194, 37.7749),
                "location_type": "city",
                "country_code": "US",
                "state_abbr": "CA",
                "city": "San Francisco",
                "parent_id": "state_1",
            },
        ]

        for location in data:
            Location.objects.update_or_create(
                id=location["id"],
                defaults={
                    "title": location["title"],
                    "center": location["center"],
                    "location_type": location["location_type"],
                    "country_code": location["country_code"],
                    "state_abbr": location["state_abbr"],
                    "city": location["city"],
                    "parent_id": Location.objects.filter(id=location.get("parent_id")).first() if location.get("parent_id") else None,
                }
            )
        self.stdout.write(self.style.SUCCESS("Successfully populated initial location data."))
