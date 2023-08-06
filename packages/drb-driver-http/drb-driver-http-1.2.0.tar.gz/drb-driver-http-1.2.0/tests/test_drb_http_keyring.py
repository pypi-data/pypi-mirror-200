import unittest
import io
from unittest.mock import patch
from multiprocessing import Process

from keyring.credentials import SimpleCredential
from requests.auth import HTTPBasicAuth

from drb.drivers.http import DrbHttpNode
from tests.utility import start_auth_serve, PORT, PATH

process = Process(target=start_auth_serve)


def my_credential(usr, pwd):
    return SimpleCredential('user', 'pwd123456')


class TestBitwardenKeyring(unittest.TestCase):
    url_ok = 'http://localhost:' + PORT + PATH + 'test.txt'

    @classmethod
    def setUpClass(cls) -> None:
        process.start()

    @classmethod
    def tearDownClass(cls) -> None:
        process.kill()

    @patch(target="keyring.get_credential", new=my_credential)
    def test_keyring_auth(self):
        node = DrbHttpNode(path=self.url_ok, auth=HTTPBasicAuth('usr', 'pwd'))

        self.assertEqual('{"path": "/resources/test.txt"}',
                         node.get_impl(io.BytesIO).getvalue().decode())
