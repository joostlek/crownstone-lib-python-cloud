import asynctest
from crownstone_cloud.lib.requestHandler import RequestHandler
from tests.mocked_replies.errors import (
    auth_error,
    access_token_expired,
    not_verified
)
from crownstone_cloud.exceptions import CrownstoneAuthenticationError


class TestCrownstoneCloud(asynctest.TestCase):
    """Test the request handler"""

    def setUp(self):
        self.request_handler = RequestHandler()

    async def test_exceptions(self):
        # mock login with errors
        with self.assertRaises(CrownstoneAuthenticationError) as login_err:
            await self.request_handler.raise_on_error(auth_error)

        assert login_err.exception.type == 'LOGIN_FAILED'

        with self.assertRaises(CrownstoneAuthenticationError) as not_verified_err:
            await self.request_handler.raise_on_error(not_verified)

        assert not_verified_err.exception.type == 'LOGIN_FAILED_EMAIL_NOT_VERIFIED'

    async def test_refresh_token(self):
        # mock access_token expired
        with asynctest.patch.object(RequestHandler, 'refresh_token') as refresh_mock:
            result = await self.request_handler.raise_on_error(access_token_expired)

        assert result is True
        refresh_mock.assert_called()
        refresh_mock.assert_awaited()