'''This module provides tests for the airodor module'''
import unittest
from ipaddress import ip_address
from yarl import URL
from airodor_wifi_api import airodor


class TestAirodorApi(unittest.TestCase):
    '''This module provides tests for the airodor module'''
    def test_get_base_url(self):
        """
        Test that the base url is correct
        """
        ipv4 = ip_address('192.168.2.122')
        refurl = URL("http://192.168.2.122/msg&Function=")
        result = airodor.get_base_api_url(ipv4)
        self.assertEqual(result, refurl)


if __name__ == '__main__':
    unittest.main()
