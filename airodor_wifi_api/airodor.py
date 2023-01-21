'''This module provides basic methods to create the api calls'''
from enum import Enum
from ipaddress import ip_address
from yarl import URL


class VentilationGroup(Enum):
    '''Basic enum to represent ventilation groups'''
    A = 1
    B = 2

    def __str__(self):
        '''convert this enum to string'''
        if self.value == self.A.value:
            return "A"
        if self.value == self.B.value:
            return "B"
        return None


class VentilationMode(Enum):
    '''Basic enum to represent the available ventilation modes'''
    OFF = 0
    ALTERNATING_MIN = 1
    ALTERNATING_MED = 2
    ALTERNATING_MAX_S = 4
    ALTERNATING_MAX_R = 6
    ONE_DIR_MED = 8
    ONE_DIR_MAX = 16
    INSIDE_MED = 32
    INSIDE_MAX = 64


def get_base_api_url(ip_addr: ip_address) -> URL:
    '''create the basic url to communicate to the wifi module'''
    return URL(f"http://{ip_addr}/msg&Function=")


def get_status(ip_addr: ip_address, group: VentilationGroup):
    '''get the current status of the ventilation'''
    print(f"getting status for group {group} from {ip_addr}")
