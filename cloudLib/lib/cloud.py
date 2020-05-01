import hashlib
import logging
import asyncio
import aiohttp
from typing import Optional, Coroutine, Any
from cloudLib._RequestHandlerInstance import RequestHandler
from cloudLib.lib.cloudModels.spheres import Spheres
from cloudLib.lib.cloudModels.crownstones import Crownstone

_LOGGER = logging.getLogger(__name__)


class CrownstoneCloud:
    """Create a Crownstone lib hub"""

    def __init__(self) -> None:
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.spheres: Optional[Spheres] = None

    def start(self, func: Coroutine) -> None:
        """Start"""
        loop = asyncio.get_event_loop()
        self.start_with_loop(func, loop)

    def start_with_loop(
            self,
            func: Coroutine,
            loop: asyncio.AbstractEventLoop
    ) -> None:
        """Start with existing loop"""
        websession = aiohttp.ClientSession(loop=loop)
        self.start_with_web_session(func, websession, loop)

    def start_with_web_session(
            self,
            func: Coroutine,
            websession: aiohttp.ClientSession,
            loop: asyncio.AbstractEventLoop
    ) -> None:
        """Start with existing web session & loop"""
        self.loop = loop
        RequestHandler.websession = websession
        self.loop.run_until_complete(func)

    async def login(self, email: str, password: str) -> None:
        """Login to Crownstone API"""
        # Create JSON object with login credentials
        data = {
            "email": email,
            "password": password_to_hash(password),
        }
        # login
        RequestHandler.login_data = data
        result = await RequestHandler.post('users', 'login', json=data)

        # Set access token & user id
        RequestHandler.access_token = result['id']
        self.spheres = Spheres(result['userId'])

        _LOGGER.info("Login to Crownstone Cloud successful")

    async def sync(self) -> None:
        """Sync all data from cloud"""
        _LOGGER.warning("Initiating all cloud data, please wait...")
        # get the sphere data
        await self.spheres.sync()

        # get the data from the sphere attributes
        for sphere in self.spheres.values():
            await asyncio.gather(
                sphere.crownstones.sync(),
                sphere.locations.sync(),
                sphere.users.sync()
            )
        _LOGGER.warning("Cloud data successfully initialized")

    def get_crownstone(self, crownstone_name) -> Crownstone:
        """Get a crownstone by name without specifying a sphere"""
        for sphere in self.spheres.values():
            for crownstone in sphere.crownstones.values():
                if crownstone.name == crownstone_name:
                    return crownstone

    def get_crownstone_by_id(self, crownstone_id) -> Crownstone:
        """Get a crownstone by id without specifying a sphere"""
        for sphere in self.spheres.values():
            return sphere.crownstones[crownstone_id]

    @staticmethod
    async def cleanup() -> None:
        """Close the websession after we are done"""
        await RequestHandler.websession.close()
        _LOGGER.warning("Session closed.")


def password_to_hash(password):
    """Generate a sha1 password from string"""
    pw_hash = hashlib.sha1(password.encode('utf-8'))
    return pw_hash.hexdigest()
