import secrets
import unittest
from daspython.auth.authenticate import DasAuth

class TestAuth(unittest.TestCase):
    def test_authenticate(self):    
        auth = DasAuth(secrets.das_url, secrets.das_username, secrets.das_password)
        success = auth.authenticate(secrets.check_https)
        self.assertEqual(success, True,f'Success should be True but got {success}.')
        
if __name__ == '__main__':
    unittest.main()

