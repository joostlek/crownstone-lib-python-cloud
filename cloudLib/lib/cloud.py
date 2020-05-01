import hashlib
import logging
import asyncio
import aiohttp
from typing import Optional, Coroutine
from cloudLib._RequestHandlerInstance import RequestHandler

_LOGGER = logging.getLogger(__name__)


class CrownstoneCloud:
    """Create a Crownstone lib hub"""

    def __init__(self) -> None:
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.user_id = None
        self.spheres = None

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
        self.user_id = result['userId']

        _LOGGER.info("Login to Crownstone Cloud successful")

    async def sync(self) -> None:
        """Sync all data from cloud"""


def password_to_hash(password):
    """Generate a sha1 password from string"""
    pw_hash = hashlib.sha1(password.encode('utf-8'))
    return pw_hash.hexdigest()
