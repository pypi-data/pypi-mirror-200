import unittest
import secrets
from daspython.auth.authenticate import DasAuth
from daspython.common.api import ApiMethods, Response, Token
from daspython.services.alcs.aclservice import AclService, ChangeOwnershipRequest


class TestAclService(unittest.TestCase):

    def _get_token(self) -> Token:
        auth = DasAuth(secrets.das_url, secrets.das_username,
                       secrets.das_password)
        auth.authenticate(secrets.check_https)
        return auth

    def test_change_ownership(self):

        acl_service = AclService(self._get_token())

        payload = ChangeOwnershipRequest()
        payload.attributeId = 55
        payload.entryId = 'f3cfd83d-b95d-4876-9217-312eec681e37'
        payload.newOwnerId = 57
        
        response = acl_service.ChangeOwnership(request=payload)

        self.assertEqual(response, True)


if __name__ == '__main__':
    unittest.main()
