"""Main class for the Crownstone cloud cloud."""
import logging
import asyncio
import aiohttp
from crownstone_cloud.cloud_models.spheres import Spheres
from crownstone_cloud.cloud_models.crownstones import Crownstone
from crownstone_cloud.helpers.requests import RequestHandler
from crownstone_cloud.helpers.logins import LoginManager
from crownstone_cloud.const import CLOUD_DATA

_LOGGER = logging.getLogger(__name__)


class CrownstoneCloud:
    """Create a Crownstone cloud instance."""

    def __init__(self, clientsession: aiohttp.ClientSession = None) -> None:
        # all data per session is stored here
        self.request_handler = RequestHandler(self, clientsession)
        self.login_manager = LoginManager(self)

    async def async_initialize(self, email: str, password: str) -> str or None:
        """
        Login to Crownstone API & synchronize all cloud data.

        This method is a coroutine.
        
        :param email: Crownstone email.
        :param password: Crownstone password.
        :return: user_id of the login.
        """
        # login
        user_id = await self.login_manager.async_login(email=email, password=password)
        _LOGGER.debug("Login to Crownstone Cloud successful")

        # get data
        await self.async_synchronize(user_id)

        return user_id

    async def async_synchronize(self, user_id: str) -> None:
        """
        Sync all data from cloud.

        This method is a coroutine.

        :param user_id: The user id of the login.
        """
        _LOGGER.debug("Initiating all cloud data")
        # get the sphere data for this user_id
        await self.get_cloud_data(user_id).async_update_sphere_data()

        # get the data from the sphere attributes
        for sphere in self.get_cloud_data(user_id):
            await asyncio.gather(
                sphere.async_update_sphere_presence(),
                sphere.crownstones.async_update_crownstone_data(),
                sphere.locations.async_update_location_data(),
                sphere.locations.async_update_location_presence(),
                sphere.users.async_update_user_data()
            )
        _LOGGER.debug("Cloud data successfully initialized")

    def get_cloud_data(self, user_id: str) -> Spheres:
        """
        Get the cloud data object for a specific logged in user.

        :param user_id: The user id of the login.
        :return: Spheres object. (Cloud data model)
        """
        self.login_manager.set_context(user_id)

        return self.login_manager.get_from_context(CLOUD_DATA)

    def get_crownstone(self, crownstone_name, user_id: str) -> Crownstone:
        """
        Get a crownstone by name without specifying a sphere.

        :param crownstone_name: Name of the Crownstone.
        :param user_id: The user id of the login.
        :return: Crownstone object.
        """
        try:
            for sphere in self.get_cloud_data(user_id):
                for crownstone in sphere.crownstones:
                    if crownstone.name == crownstone_name:
                        return crownstone
        except KeyError:
            _LOGGER.exception("This login_id does not exist. Use 'async_login' to login.")
        except ValueError:
            _LOGGER.exception("No sphere data available for this login. Use 'async_synchronize' to load user data.")

    def get_crownstone_by_id(self, crownstone_id, user_id: str) -> Crownstone:
        """
        Get a crownstone by id without specifying a sphere.

        :param crownstone_id: The cloud id of the Crownstone.
        :param user_id: The user id of the login.
        :return: Crownstone object.
        """
        try:
            for sphere in self.get_cloud_data(user_id):
                return sphere.crownstones[crownstone_id]
        except KeyError:
            _LOGGER.exception("This login_id does not exist. Use 'async_login' to login.")
        except ValueError:
            _LOGGER.exception("No sphere data available for this login. Use 'async_synchronize' to load user data.")

    async def async_close_session(self) -> None:
        """
        Close the aiohttp clientsession after all requests are done.

        The session should always be closed when the program ends.
        When there's an external clientsession in use, DON'T use this method.

        This method is a coroutine.
        """
        await self.request_handler.client_session.close()
