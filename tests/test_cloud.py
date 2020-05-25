import asynctest
import asyncio
import aiohttp
from crownstone_cloud.lib.cloud import CrownstoneCloud
from crownstone_cloud._RequestHandlerInstance import RequestHandler
from tests.mocked_replies.login_data import login_data
from tests.mocked_replies.sphere_data import (
    sphere_data,
    key_data,
    expected_key_data,
)
from tests.mocked_replies.crownstone_data import (
    crownstone_data,
    switch_state_data,
)
from tests.mocked_replies.user_data import user_data
from tests.mocked_replies.location_data import (
    location_data,
    presence_data
)
from crownstone_cloud.lib.cloudModels.spheres import Spheres


class TestCrownstoneCloud(asynctest.TestCase):
    """Test the main class"""

    def setUp(self):
        self.cloud = CrownstoneCloud('email', 'password')
        self.test_loop = asyncio.new_event_loop()
        self.test_websession = aiohttp.ClientSession(loop=self.test_loop)

    def test_init(self):
        assert self.cloud.loop == asyncio.get_event_loop()
        assert isinstance(RequestHandler.websession, aiohttp.ClientSession)

        self.cloud = CrownstoneCloud('email', 'password', loop=self.test_loop)
        assert self.cloud.loop == self.test_loop

        self.cloud = CrownstoneCloud('email', 'password', loop=self.test_loop, websession=self.test_websession)
        assert RequestHandler.websession == self.test_websession

    async def test_initialize(self):
        # test init, only logging in when there's no access token
        with asynctest.patch.object(CrownstoneCloud, 'login') as login_mock:
            with asynctest.patch.object(CrownstoneCloud, 'sync') as sync_mock:
                await self.cloud.initialize()
        # test called and awaited
        login_mock.assert_called()
        login_mock.assert_awaited()
        # test called and awaited
        sync_mock.assert_called()
        sync_mock.assert_awaited()

        RequestHandler.access_token = 'access_token'

        with asynctest.patch.object(CrownstoneCloud, 'login') as login_mock:
            with asynctest.patch.object(CrownstoneCloud, 'sync') as sync_mock:
                await self.cloud.initialize()
        # test not called
        login_mock.assert_not_called()
        # test called and awaited
        sync_mock.assert_called()
        sync_mock.assert_awaited()

    def test_set_access_token(self):
        self.cloud.set_access_token('new_access_token')
        assert RequestHandler.access_token == 'new_access_token'

    @asynctest.patch.object(RequestHandler, 'post')
    async def test_login(self, mock_request):
        # patch the result of login request
        mock_request.return_value = login_data
        await self.cloud.login()
        assert RequestHandler.access_token == 'my_access_token'
        assert self.cloud.spheres.user_id == 'user_id'

    @asynctest.patch.object(RequestHandler, 'get')
    async def test_data_structure(self, mock_request):
        # create fake instance
        self.cloud.spheres = Spheres(self.test_loop, 'user_id')
        # add fake sphere data for test
        mock_request.return_value = sphere_data
        await self.cloud.spheres.update()
        mock_request.assert_awaited()

        # test getting a sphere by id and name
        sphere = self.cloud.spheres.find_by_id('my_awesome_sphere_id2')
        assert sphere.cloud_id == 'my_awesome_sphere_id2'
        sphere2 = self.cloud.spheres.find('my_awesome_sphere')
        assert sphere2.name == 'my_awesome_sphere'

        # test getting keys
        mock_request.return_value = key_data
        keys = await sphere.get_keys()
        mock_request.assert_awaited()
        assert keys == expected_key_data

        # add fake crownstone data for test
        mock_request.return_value = crownstone_data
        await sphere.crownstones.update()
        mock_request.assert_awaited()
        # state
        mock_request.return_value = switch_state_data
        await sphere.crownstones.update_state()
        mock_request.assert_awaited()

        # add fake user data for test
        mock_request.return_value = user_data
        await sphere.users.update()
        mock_request.assert_awaited()

        # add fake location data for test
        mock_request.return_value = location_data
        await sphere.locations.update()
        mock_request.assert_awaited()
        # presence
        mock_request.return_value = presence_data
        await sphere.locations.update_presence()
        mock_request.assert_awaited()

        # test getting crownstone, users, locations by id & name
        crownstone = sphere.crownstones.find('my_awesome_crownstone')
        crownstone_by_id = sphere.crownstones.find_by_id('my_awesome_crownstone_id2')
        assert crownstone.name == 'my_awesome_crownstone'
        assert crownstone_by_id.cloud_id == 'my_awesome_crownstone_id2'
        # test state
        assert crownstone.state == 0

        location = sphere.locations.find('my_awesome_location_1')
        location_by_id = sphere.locations.find_by_id('my_awesome_location_id_3')
        assert location.cloud_id == 'my_awesome_location_id_1'
        assert location_by_id.name == 'my_awesome_location_3'
        # test presence
        assert len(location.present_people) == 1
        assert len(location_by_id.present_people) == 1

        user_first = sphere.users.find_by_first_name('I am')
        user_last = sphere.users.find_by_last_name('Awesome')
        user_by_id = sphere.users.find_by_id('we_are_awesome_id')
        assert 'You are' and 'We are' not in user_first
        assert len(user_last) == 3
        assert user_by_id.first_name == 'We are'
        assert user_by_id.last_name == 'Awesome'

        # test setting brightness of a crownstone
        with asynctest.patch.object(RequestHandler, 'put') as brightness_mock:
            # test if it doesn't run if dimming not enabled
            await crownstone.set_brightness(50)
            brightness_mock.assert_not_called()
            # set dimming to true for test
            crownstone.dimming_enabled = True
            with self.assertRaises(ValueError):
                await crownstone.set_brightness(200)