"""Manager that manages logins into the Crownstone API."""
import logging
from typing import Optional, Dict, Any
from crownstone_cloud.helpers.conversion import password_to_hash
from crownstone_cloud.exceptions import CrownstoneDataError, DataError
from crownstone_cloud.cloud_models.spheres import Spheres
from crownstone_cloud.const import (
    LOGIN_DATA,
    CLOUD_DATA,
    ACCESS_TOKEN
)

_LOGGER = logging.getLogger(__name__)


class LoginManager:
    """Manager for logins to the Crownstone Cloud."""

    def __init__(self, cloud) -> None:
        """Initialize the login manager."""
        self.cloud = cloud
        self._context: str = str()
        self.logins: Dict[str, Optional[Dict[str, Any]]] = {}

    def get_access_token(self, user_id: str) -> str or None:
        """Get the access token for an existing login."""
        return self.logins[user_id][ACCESS_TOKEN]

    async def async_login(self, email: str, password: str) -> str:
        """Login to the Crownstone Cloud, save access token and return user id."""
        login_data = {
            'email': email,
            'password': password_to_hash(password)
        }

        # check if login data already exists
        for login in self.logins.values():
            if login.get(LOGIN_DATA) == login_data:
                raise CrownstoneDataError(DataError['ALREADY_EXISTS'], "User is already logged in")

        login_response = await self.cloud.request_handler.request_login(login_data)
        user_id = login_response['userId']
        access_token = login_response['id']

        # save data for user
        self.logins[user_id] = {}
        self.logins[user_id][LOGIN_DATA] = login_data
        self.logins[user_id][ACCESS_TOKEN] = access_token
        self.logins[user_id][CLOUD_DATA] = Spheres(self.cloud, user_id)

        return user_id

    def get_context(self) -> str:
        """
        Get the current context.

        Used when objects were created in a certain context.
        """
        return self._context

    def set_context(self, user_id: str) -> None:
        """Set the current user context.

        Functions can simply request which user id is currently requested, 
        instead of appending it as parameter everywhere.
        """
        self._context = user_id

    def get_from_context(self, key: str) -> Any:
        """Get the current user context."""
        try:
            return self.logins.get(self._context).get(key)
        except (KeyError, ValueError):
            raise CrownstoneDataError(DataError['DOES_NOT_EXIST'],
                                      "Data not found for user, use one of the constants defined in "
                                      "crownstone_cloud/const.")

    def set_in_context(self, key: str, value: Any) -> None:
        """Set a new value for a key in a certain context."""
        try:
            self.logins.get(self._context)[key] = value
        except (KeyError, ValueError):
            raise CrownstoneDataError(DataError['DOES_NOT_EXIST'], "Error setting value for this key. use one of the "
                                                                   "constants defined in "
                                                                   "crownstone_cloud/const.")
