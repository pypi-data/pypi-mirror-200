from daspython.services.attributes.attributeservice import AttributeService
import secrets
import unittest
from daspython.auth.authenticate import DasAuth
from daspython.services.attributes.attributeservice import AttributeService

class TestAttributeService(unittest.TestCase):

    def test_get_attribute_name(self):

        auth = DasAuth(secrets.das_url, secrets.das_username, secrets.das_password)
        auth.authenticate(secrets.check_https)

        service = AttributeService(auth)        
        result = service.get_attribute_name(55)

        self.assertEqual(result, 'Core',f'Expected value is Core but got {result}')

    def test_get_attribute_id(self):

        auth = DasAuth(secrets.das_url, secrets.das_username, secrets.das_password)
        auth.authenticate(secrets.check_https)

        service = AttributeService(auth)        
        result = service.get_attribute_id('Core')
        
        self.assertEqual(result, 55,f'Expected value is 55 but got {result}')        


if __name__ == '__main__':
    unittest.main()        