import os
import unittest
from unittest import mock

from app.core.security import RateLimiter, check_api_key, is_production


class SecurityLayerTests(unittest.TestCase):
    def test_api_key_validation(self):
        self.assertTrue(check_api_key('secret', 'secret'))
        self.assertFalse(check_api_key('secret', 'wrong'))
        self.assertTrue(check_api_key(None, None))

    def test_unconfigured_key_is_open_only_outside_production(self):
        self.assertTrue(check_api_key(None, None, production=False))
        self.assertFalse(check_api_key(None, None, production=True))
        self.assertFalse(check_api_key('anything', None, production=True))

    def test_configured_key_still_enforced_in_production(self):
        self.assertTrue(check_api_key('secret', 'secret', production=True))
        self.assertFalse(check_api_key('wrong', 'secret', production=True))
        self.assertFalse(check_api_key(None, 'secret', production=True))

    def test_is_production_parses_common_truthy_values(self):
        for value in ('1', 'true', 'TRUE', 'yes', 'on', ' true '):
            with mock.patch.dict(os.environ, {'PRODUCTION': value}):
                self.assertTrue(is_production(), value)
        for value in ('', '0', 'false', 'no'):
            with mock.patch.dict(os.environ, {'PRODUCTION': value}):
                self.assertFalse(is_production(), value)

    def test_rate_limiter_blocks_excess_requests(self):
        limiter = RateLimiter(limit=2, window_seconds=60)
        self.assertTrue(limiter.allow('client-a'))
        self.assertTrue(limiter.allow('client-a'))
        self.assertFalse(limiter.allow('client-a'))


if __name__ == '__main__':
    unittest.main()
