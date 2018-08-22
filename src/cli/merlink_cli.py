# -*- coding: utf-8 -*-
# Copyright 2018 Ross Jacobs All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provides a CLI for MerLink"""
import argparse

from src.cli.cli_modal_prompts import CliModalPrompts
from src.modules.dashboard_browser import DataScraper


class MainCli:
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
    Usage: merlink --username <username> --password <password> --organization
    <organization> --network <network> --options <options>

    ex. merlink --username 'wile.e.coyote@acme.corp' --password 'SuperGenius!'
        --organization 'ACME Corp' --network 'Wild West'

    NOTE: If there are conflicts in organization or network names, there will
    be an error and it may be wise to use organization_id/network_id instead.
    """

    def __init__(self):
        super(MainCli, self).__init__()

        self.parse_options()
        self.messages = CliModalPrompts()
        self.browser = DataScraper()

    @staticmethod
    def parse_options():
        """Parses argparse options and then calls other parts of program."""

        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose",
                            help="increase output verbosity",
                            action="store_true")

        required_group = parser.add_argument_group("required arguments")
        required_group.add_argument(
            "-o", "--organization-id",
            help="The Dashboard organization id for the firewall (like "
                 "'123456'). To get this value for your firewall, use the API",
            required=True)
        required_group.add_argument(
            "-n", "--network-id",
            help="The Dashboard network id for the firewall (like aBc123d). "
                 "To get this value for your firewall, use the API.",
            required=True)
        required_group.add_argument(
            "-u", "--username",
            help="The Dashboard email account that you login with. This "
                 "account should have access to the firewall to which "
                 "you want to connect.",
            required=True)
        required_group.add_argument(
            "-p", "--password",
            help="Your Dashboard account password.",
            required=True)

        args = parser.parse_args()
        if args.verbose:
            print("Welcome to Merlink Verbose!")
            # 60w and 80w ASCII Miles generated by
            # https://www.ascii-art-generator.org/
            # 48w made by hand with ASCII characters
            with open("src/media/ascii-miles-48w.txt", 'r') as miles:
                print(miles.read())
            exit()

    def show_main_menu(self):
        """Shows the main cli menu

        Currently not implemented but mirrored in main_window"""

        pass

    def get_user_action(self):
        """Gets the user's next action

        Currently not implemented but mirrored in main_window"""

        pass

    def add_vpn(self):
        """Adds a vpn by name

        Currently not implemented but mirrored in main_window"""

        pass

    def connect_vpn(self, *vpn_vars):
        """Connects using the specified vpn connection

        Currently not implemented but mirrored in main_window"""

        pass

    def show_result(self, result):
        """Shows the result of the vpn connection to the console

        Currently not implemented but mirrored in main_window"""

        pass

    def troubleshoot_vpn(self):
        """Provides a

        Currently not implemented but mirrored in main_window"""

        pass
