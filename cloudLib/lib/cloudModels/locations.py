from cloudLib._RequestHandlerInstance import RequestHandler
from typing import Optional


class Locations:
    """Handler for the locations of a sphere"""

    def __init__(self, sphere_id: str) -> None:
        """Init"""
        self.locations = {}
        self.sphere_id = sphere_id

    async def sync(self) -> None:
        """Get the locations and presence from the cloud"""
        location_data = await RequestHandler.get('Spheres', 'ownedLocations', model_id=self.sphere_id)
        for location in location_data:
            self.locations[location['id']] = Location(location)

        presence_data = await RequestHandler.get('Spheres', 'presentPeople', model_id=self.sphere_id)
        for presence in presence_data:
            for present_location in presence['locations']:
                for location in self.locations.values():
                    if present_location == location.cloud_id:
                        location.present_people.append(presence['userId'])

    def find(self, location_name: str) -> object or None:
        """Search for a sphere by name and return sphere object if found"""
        for location in self.locations.values():
            if location_name == location.name:
                return location

        return None

    def find_by_id(self, location_id: str) -> object or None:
        """Search for a sphere by id and return sphere object if found"""
        return self.locations[location_id]


class Location:
    """Represents a location"""

    def __init__(self, data: dict):
        self.data = data
        self.present_people = []

    @property
    def name(self) -> str:
        return self.data['name']

    @property
    def cloud_id(self) -> str:
        return self.data['id']

    @property
    def unique_id(self) -> int:
        return self.data['uid']
