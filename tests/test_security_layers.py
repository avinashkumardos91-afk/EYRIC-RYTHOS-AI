import unittest

from app.core.security import RateLimiter, check_api_key


class SecurityLayerTests(unittest.TestCase):
    def test_api_key_validation(self):
        self.assertTrue(check_api_key('secret', 'secret'))
        self.assertFalse(check_api_key('secret', 'wrong'))
        self.assertTrue(check_api_key(None, None))

    def test_rate_limiter_blocks_excess_requests(self):
        limiter = RateLimiter(limit=2, window_seconds=60)
        self.assertTrue(limiter.allow('client-a'))
        self.assertTrue(limiter.allow('client-a'))
        self.assertFalse(limiter.allow('client-a'))


if __name__ == '__main__':
    unittest.main()
