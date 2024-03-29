'''This module provides tests for the airodor module'''
import unittest
from datetime import datetime
from ipaddress import ip_address

import requests
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
        self.assertEqual(result, URL("http://192.168.2.122/msg?Function="))

    def test_get_request_url_write(self):
        """
        Test to write a mode to a group
        """
        ipv4 = ip_address('192.168.2.122')
        result = airodor.get_request_url(
            ip_addr=ipv4,
            action=airodor.VentilationAction.WRITE_MODE,
            group=airodor.VentilationGroup.A,
            mode=airodor.VentilationModeSet.ALTERNATING_MAX,
        )
        self.assertEqual(result, URL("http://192.168.2.122/msg?Function=WA4"))
        result = airodor.get_request_url(
            ip_addr=ipv4,
            action=airodor.VentilationAction.WRITE_MODE,
            group=airodor.VentilationGroup.A,
            mode=airodor.VentilationModeSet.ALTERNATING_MED,
        )
        self.assertEqual(result, URL("http://192.168.2.122/msg?Function=WA2"))

    def test_get_request_url_read(self):
        """
        Test to read a mode from a group
        """
        ipv4 = ip_address('192.168.2.122')
        result = airodor.get_request_url(
            ip_addr=ipv4, action=airodor.VentilationAction.READ_MODE, group=airodor.VentilationGroup.A
        )
        self.assertEqual(result, URL("http://192.168.2.122/msg?Function=RA"))
        result = airodor.get_request_url(
            ip_addr=ipv4, action=airodor.VentilationAction.READ_MODE, group=airodor.VentilationGroup.B
        )
        self.assertEqual(result, URL("http://192.168.2.122/msg?Function=RB"))

    def test_interpret_answer(self):
        """
        Test to interpret the answer from the module
        """
        r = requests.Response
        r.ok = True

        r.text = "RB0"
        a, b = airodor.interpret_answer(r)
        self.assertEqual(a, airodor.VentilationGroup.B)
        self.assertEqual(b, airodor.VentilationModeRead.OFF)

        r.text = "RA66"
        a, b = airodor.interpret_answer(r)
        self.assertEqual(a, airodor.VentilationGroup.A)
        self.assertEqual(b, airodor.VentilationModeRead.INSIDE_MAX)

        # test reading a "set" value, might occur right after setting and reading the mode
        r.text = "RA64"
        a, b = airodor.interpret_answer(r)
        self.assertEqual(a, airodor.VentilationGroup.A)
        self.assertEqual(b, airodor.VentilationModeSet.INSIDE_MAX)

        r.text = "MAOK"
        a, b = airodor.interpret_answer(r)
        self.assertEqual(a, airodor.VentilationGroup.A)
        self.assertEqual(b, True)

        r.text = "MBNOOK"
        a, b = airodor.interpret_answer(r)
        self.assertEqual(a, airodor.VentilationGroup.B)
        self.assertEqual(b, False)

    def test_timer_list(self):
        ventlist = airodor.VentilationTimerList()
        ventlist.add_list_item(
            # 1.11.2011 11:11:11 -> fourth entry
            datetime(year=2011, month=11, day=1, hour=11, minute=11, second=11),
            airodor.VentilationGroup.A,
            airodor.VentilationModeSet.INSIDE_MAX,
        )
        ventlist.add_list_item(
            # 1.10.2011 11:11:11 -> third entry
            datetime(year=2011, month=10, day=1, hour=11, minute=11, second=11),
            airodor.VentilationGroup.A,
            airodor.VentilationModeSet.ALTERNATING_MAX,
        )
        ventlist.add_list_item(
            # 1.11.2010 11:11:10 -> first entry
            datetime(year=2010, month=11, day=1, hour=11, minute=11, second=10),
            airodor.VentilationGroup.A,
            airodor.VentilationModeSet.ALTERNATING_MED,
        )
        ventlist.add_list_item(
            # 1.11.2010 11:11:11 -> second entry
            datetime(year=2010, month=11, day=1, hour=11, minute=11, second=11),
            airodor.VentilationGroup.A,
            airodor.VentilationModeSet.ALTERNATING_MIN,
        )

        # order of VentilationMode should be:
        # ALTERNATING_MED, ALTERNATING_MIN, ALTERNATING_MAX, INSIDE_MAX
        self.assertEqual(ventlist.timer_list[0].mode, airodor.VentilationModeSet.ALTERNATING_MED)
        self.assertEqual(ventlist.timer_list[1].mode, airodor.VentilationModeSet.ALTERNATING_MIN)
        self.assertEqual(ventlist.timer_list[2].mode, airodor.VentilationModeSet.ALTERNATING_MAX)
        self.assertEqual(ventlist.timer_list[3].mode, airodor.VentilationModeSet.INSIDE_MAX)

        next_item = ventlist.pop_list_item()
        self.assertEqual(next_item.mode, airodor.VentilationModeSet.ALTERNATING_MED)
        self.assertEqual(ventlist.timer_list[0].mode, airodor.VentilationModeSet.ALTERNATING_MIN)
        self.assertEqual(ventlist.timer_list[1].mode, airodor.VentilationModeSet.ALTERNATING_MAX)
        self.assertEqual(ventlist.timer_list[2].mode, airodor.VentilationModeSet.INSIDE_MAX)


if __name__ == '__main__':
    unittest.main()
