import secrets
import unittest

from requests.api import request
from daspython.common.api import Token
from daspython.auth.authenticate import DasAuth
from daspython.services.entryfields.entryfieldservice import EntryFieldService, DisplayType


class TestEntryService(unittest.TestCase):
    def _get_token(self) -> Token:
        auth = DasAuth(secrets.das_url, secrets.das_username,
                       secrets.das_password)
        auth.authenticate(secrets.check_https)
        return auth

    def test_getall(self):

       service = EntryFieldService(self._get_token())       
       response = service.get_all(55, DisplayType.FORM)
       self.assertGreater(response.total, 0, f'EntryFieldService - Get All function should return totalCount greater than 0.')


if __name__ == '__main__':
    unittest.main()
