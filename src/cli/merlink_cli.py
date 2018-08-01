#!/usr/bin/python3

"""
MerLink CLI
Based on ncurses


Command line options based on expected use cases:

1. To enter all information manually
Usage: merlink --name <vpn name> --address <server IP/FQDN> --psk <PSK>
   --username <username> --password <password>

ex. merlink --name 'ACME VPN' --address 'acme.corp' --psk '@AnyCost'
    --username 'wile.e.coyote@acme.corp' --password 'SuperGenius!'

2. Interactive mode: If dashboard username/password are known
Usage: merlink --username <username> --password <password>
<< Organizations and networks are shown to user
>> User selects the network they would like to connect to
<< program creates and connects vpn

3. If username + password of dashboard admin, organization name, and
network name are already known
Usage: merlink --username <username> --password <password>
    --organization <organization> --network <network> --options <options>

ex. merlink --username 'wile.e.coyote@acme.corp' --password 'SuperGenius!'
    --organization 'ACME Corp' --network 'Wild West'

NOTE: If there are conflicts in organization or network names, there will be an
error and it may be wise to use organization_id/network_id instead.
"""

import argparse
from src.cli.modal_prompts import ModalPrompts
from src.modules.dashboard_browser import DataScraper


class MainCli:
    def __init__(self):
        super(MainCli, self).__init__()

        self.parse_options()
        self.messages = ModalPrompts()
        self.browser = DataScraper()

    @staticmethod
    def parse_options():
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose", help="increase output verbosity",
                            action="store_true")
        args = parser.parse_args()
        if args.verbose:
            print("Welcome to Merlink Verbose!")
            # 60w and 80w ASCII Miles generated by
            # https://www.ascii-art-generator.org/
            # 48w made by hand with ASCII characters
            with open("src/media/ascii-miles-48w.txt", 'r') as miles:
                print(miles.read())

    def login_provider(self):
        pass

    def show_main_menu(self):
        pass

    def get_user_action(self): pass

    def add_vpn(self): pass

    def connect_vpn(self, *vpn_vars):
        pass

    def show_result(self, result):
        pass

    def troubleshoot_vpn(self): pass
