from cloudLib._RequestHandlerInstance import RequestHandler
from cloudLib.lib.cloudModels.crownstones import Crownstones
from cloudLib.lib.cloudModels.locations import Locations
from cloudLib.lib.cloudModels.users import Users
from cloudLib.lib.containerClasses.keys import Keys
from typing import Optional, ValuesView


class Spheres:
    """Handler for the spheres of the user"""

    def __init__(self, user_id: str) -> None:
        """Init"""
        self.spheres = {}
        self.user_id = user_id

    def values(self) -> ValuesView:
        """Return a view with the sphere objects in dict, for iteration"""
        return self.spheres.values()

    async def sync(self) -> None:
        """Get the spheres for the user from the cloud"""
        sphere_data = await RequestHandler.get('users', 'spheres', model_id=self.user_id)
        for sphere in sphere_data:
            self.spheres[sphere['id']] = Sphere(sphere)

    def find(self, sphere_name: str) -> object or None:
        """Search for a sphere by name and return sphere object if found"""
        for sphere in self.spheres.values():
            if sphere_name == sphere.name:
                return sphere

        return None

    def find_by_id(self, sphere_id: str) -> object or None:
        """Search for a sphere by id and return sphere object if found"""
        return self.spheres[sphere_id]

    async def get_keys(self) -> None:
        """Get the user keys for the spheres, that can be used for BLE (optional)"""
        keys = await RequestHandler.get('users', 'keysV2', model_id=self.user_id)
        for key_set in keys:
            for sphere in self.spheres:
                if key_set['sphereId'] == sphere.cloud_id:
                    sphere.keys = Keys(key_set)


class Sphere:
    """Represents a Sphere"""

    def __init__(self, data: dict):
        self.data = data
        self.crownstones = Crownstones(self.cloud_id)
        self.locations = Locations(self.cloud_id)
        self.users = Users(self.cloud_id)
        self.keys: Optional[Keys] = None

    @property
    def name(self) -> str:
        return self.data['name']

    @property
    def cloud_id(self) -> str:
        return self.data['id']

    @property
    def unique_id(self) -> int:
        return self.data['uid']
