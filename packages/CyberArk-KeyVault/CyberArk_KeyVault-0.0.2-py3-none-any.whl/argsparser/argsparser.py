__author__="Ayush Yajnik"

import argparse
import sys

sys.path.append('..')

from constants.runargs import Args

args = None

def parse_args():
    global args

    parser = argparse.ArgumentParser()

    parser.add_argument('--{}'.format(Args.CYBERARK_HOST.value),'-cyberArk_host',help="Host details for retrieving the password and other details")
    parser.add_argument('--{}'.format(Args.APPID.value),'-appID',help="App ID for entering into CyberArk")
    parser.add_argument('--{}'.format(Args.SAFE.value),'-safe',help="Safe ID for entering into CyberArk")
    parser.add_argument('--{}'.format(Args.CYBERARK_USERNAME.value),'-cyberark_usr',help="CyberArk username for authentication")
    parser.add_argument('--{}'.format(Args.SAFE.value),'-safe',help="Safe ID for entering into CyberArk")
    parser.add_argument('--{}'.format(Args.SAFE.value),'-safe',help="oBJECT ID for an account in CyberArk")
    args = vars(parser.parse_args())

    return args

def get_run_args(key):
    parse_args()
    return args[key]


    
    
    