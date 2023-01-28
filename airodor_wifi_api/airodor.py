'''This module provides basic methods to create the api calls'''
from enum import Enum
from ipaddress import ip_address
from yarl import URL
import requests


class VentilationGroup(Enum):
    '''Basic enum to represent ventilation groups'''
    A = "A"
    B = "B"


class VentilationAction(Enum):
    '''Basic enum to represent ventilation actions'''
    READ_MODE = "R"
    WRITE_MODE = "W"
    READ_OFF_TIMER = "T"
    SET_OFF_TIMER = "S"


class VentilationMode(Enum):
    '''Basic enum to represent the available ventilation modes'''
    OFF = 0
    ALTERNATING_MIN = 1
    ALTERNATING_MED = 2
    ALTERNATING_MAX = 46
    ALTERNATING_MAX_S = 4
    ALTERNATING_MAX_R = 6
    ONE_DIR_MED = 8
    ONE_DIR_MAX = 16
    INSIDE_MED = 32
    INSIDE_MAX = 64


class VentilationAnswerType(Enum):
    '''Basic enum to represent the available answer types'''
    R = "R"
    M = "M"
    T = "T"
    S = "S"


def get_base_api_url(ip_addr: ip_address) -> URL:
    '''create the basic url to communicate to the wifi module'''
    return URL(f"http://{ip_addr}/msg?Function=")


def get_request_url(ip_addr: ip_address,
                    action: VentilationAction,
                    group: VentilationGroup,
                    mode: VentilationMode = "") -> URL:
    '''create url for the required action, group and mode'''
    url = get_base_api_url(ip_addr=ip_addr)
    if mode == VentilationMode.ALTERNATING_MAX_R:
        assert action == VentilationAction.READ_MODE
    if mode == VentilationMode.ALTERNATING_MAX_S:
        assert action == VentilationAction.WRITE_MODE
    if mode == VentilationMode.ALTERNATING_MAX:
        if action == VentilationAction.READ_MODE:
            mode = VentilationMode.ALTERNATING_MAX_R
        elif action == VentilationAction.WRITE_MODE:
            mode = VentilationMode.ALTERNATING_MAX_S

    if action == VentilationAction.WRITE_MODE:
        assert VentilationMode != ""
        return URL(f"{url}{action.value}{group.value}{mode.value}")
    if action == VentilationAction.READ_MODE:
        return URL(f"{url}{action.value}{group.value}")

    raise NotImplementedError(
        f"VentilationAction {action} is not yet implemented")


def interpret_answer(answer: requests.Response) -> tuple:
    '''interpret the request answer from the wifi module.
    For READ, the return is (group, mode).
    For WRITE, the return is (group, OK?)'''
    # assert that the answer is valid
    assert answer.ok
    # first character is always answer type
    vat = VentilationAnswerType(answer.text[0])
    # second character is always group
    group = VentilationGroup(answer.text[1])

    if vat == VentilationAnswerType.R:
        # for read type, the character 2+ is the ventilation mode
        return group, VentilationMode(int(answer.text[2:]))
    if vat == VentilationAnswerType.M:
        # for write type, the character 2+ is the "OK" notifier
        return group, (answer.text[2:] == "OK")

    raise NotImplementedError(
        f"VentilationAnswer for {vat} is not yet implemented")


def get_mode(ip_addr: ip_address, group: VentilationGroup)\
        -> VentilationMode:
    '''get the current mode for the given ip and ventilation group'''
    print(f"getting status for group {group} from {ip_addr}")
    request = get_request_url(ip_addr=ip_addr,
                              action=VentilationAction.READ_MODE,
                              group=group)
    r = requests.get(str(request))
    r_group, r_mode = interpret_answer(r)
    assert r_group == group  # answer should fit to the request
    return r_mode
