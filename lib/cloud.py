import hashlib
import logging
import asyncio
from typing import Optional, Dict
from aiohttp import ClientSession
from lib.requestHandler import RequestHandler

_LOGGER = logging.getLogger(__name__)


class CrownstoneCloud:
    """Create a Crownstone lib hub"""

    def __init__(self) -> None:
        self.websession: Optional[ClientSession] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.request: Optional[RequestHandler] = None
        # Instance information
        self.access_token = None
        self.user_id = None

    def start(self, func):
        """Start"""

    def start_with_loop(self, func, loop):
        """Start"""

    def start_with_web_session(self, func, websession, loop):
        """Start"""

    async def login(self, email: str, password: str) -> None:
        """Login to Crownstone API"""
        # Create JSON object with login credentials
        data = {
            "email": email,
            "password": password_to_hash(password),
        }
        # Login to lib
        result = await self.request.post('users', 'login', json=data)

        # Set access token & user id
        self.access_token = result['id']
        self.user_id = result['userId']

        _LOGGER.info("Login to Crownstone Cloud successful")


def password_to_hash(password):
    """Generate a sha1 password from string"""
    pw_hash = hashlib.sha1(password.encode('utf-8'))
    return pw_hash.hexdigest()
