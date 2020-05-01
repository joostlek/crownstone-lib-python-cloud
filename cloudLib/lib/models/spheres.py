from cloudLib._RequestHandlerInstance import RequestHandler


class Spheres:
    """Handler for the spheres of the user"""

    def __init__(self, user_id: str) -> None:
        """Init"""
        self.spheres = {}
        self.user_id = user_id

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

    def update(self, event_data) -> None:
        """Update sphere data using event data"""


class Sphere:
    """Represents a Sphere"""

    def __init__(self, data):
        self.data = data
        self.crownstones = None
        self.locations = None

    @property
    def name(self) -> str:
        return self.data['name']

    @property
    def cloud_id(self) -> str:
        return self.data['id']

    @property
    def unique_id(self) -> int:
        return self.data['uid']
