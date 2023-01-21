'''This module provides basic methods to create the api calls'''
from enum import Enum

class VentilationGroup(Enum):
    '''Basic enum to represent ventilation groups'''
    A = 1
    B = 2

    def __str__(self):
        '''convert this enum to string'''
        if self.value == self.A.value:
            return "A"
        elif self.value == self.B.value:
            return "B"
        else:
            return None

def get_status(ip_address:str, group:VentilationGroup):
    '''get the current status of the ventilation'''
    print("getting status for group {} from {}".format(group, ip_address))
