__author__="Ayush Yajnik"

from enum import Enum,unique
import sys

sys.path.append('..')

@unique
class Args(Enum):
    CYBERARK_HOST = 'cyberark_host'
    APPID = 'core_appid'
    SAFE = 'core_safe'
    CA_OBJECT = 'core_obj'
    CYBERARK_USERNAME = 'cyberark_username'