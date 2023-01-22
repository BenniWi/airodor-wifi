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
        result = airodor.get_base_api_url(ipv4)
        self.assertEqual(result, URL("http://192.168.2.122/msg&Function="))

    def test_get_request_url_write(self):
        """
        Test to write a mode to a group
        """
        ipv4 = ip_address('192.168.2.122')
        result = airodor.get_request_url(
            ip_addr=ipv4,
            action=airodor.VentilationAction.WRITE_MODE,
            group=airodor.VentilationGroup.A,
            mode=airodor.VentilationMode.ALTERNATING_MAX)
        self.assertEqual(result, URL("http://192.168.2.122/msg&Function=WA4"))
        result = airodor.get_request_url(
            ip_addr=ipv4,
            action=airodor.VentilationAction.WRITE_MODE,
            group=airodor.VentilationGroup.A,
            mode=airodor.VentilationMode.ALTERNATING_MED)
        self.assertEqual(result, URL("http://192.168.2.122/msg&Function=WA2"))

    def test_get_request_url_read(self):
        """
        Test to read a mode from a group
        """
        ipv4 = ip_address('192.168.2.122')
        result = airodor.get_request_url(
            ip_addr=ipv4,
            action=airodor.VentilationAction.READ_MODE,
            group=airodor.VentilationGroup.A)
        self.assertEqual(result, URL("http://192.168.2.122/msg&Function=RA"))
        result = airodor.get_request_url(
            ip_addr=ipv4,
            action=airodor.VentilationAction.READ_MODE,
            group=airodor.VentilationGroup.B)
        self.assertEqual(result, URL("http://192.168.2.122/msg&Function=RB"))


if __name__ == '__main__':
    unittest.main()
