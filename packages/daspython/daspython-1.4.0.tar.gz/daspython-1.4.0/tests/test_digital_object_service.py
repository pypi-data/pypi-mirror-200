import unittest
import secrets

from daspython.common.api import Token
from daspython.auth.authenticate import DasAuth
from daspython.services.digitalobjects.digitalobjectservice import DigitalObjectService, UploadDigitalObjectRequest


class TestDigitalObjectService(unittest.TestCase):
    
    def _get_token(self) -> Token:
        auth = DasAuth(secrets.das_url, secrets.das_username,
                       secrets.das_password)
        auth.authenticate(secrets.check_https)
        return auth

    def test_upload_digital_object(self):

        digital_object_service = DigitalObjectService(self._get_token())

        request = UploadDigitalObjectRequest()
        request.entryCode = 'zb.b.9w'
        request.filePath = 'C:\\Temp\\TEST-01.txt'
        request.description = 'Uploaded from Python'
        digital_object_service.upload(request)

    def test_link_existing(self):
         digital_object_service = DigitalObjectService(self._get_token())
         digital_object_service.link_existing(self.ENTRY_CODE,'h.b.wq3c')

    def test_download_request(self):
        digital_object_service = DigitalObjectService(self._get_token())
        digital_object_service.download_request('zb.b.tw')

    def test_download_request_one_file(self):
        digital_object_service = DigitalObjectService(self._get_token())
        digital_object_service.download_request('zb.b.tw', ['h.b.n9bh'])

    def test_get_my_requests(self):
        digital_object_service = DigitalObjectService(self._get_token())
        download_resquests = digital_object_service.get_my_requests()
        self.assertGreater(download_resquests.total_count, 0,
                           f'Download requests must be greater than 0.')

    def test_get_my_files(self):
        digital_object_service = DigitalObjectService(self._get_token())
        download_request_response = digital_object_service.get_files_from_download_request()


if __name__ == '__main__':
    unittest.main()
