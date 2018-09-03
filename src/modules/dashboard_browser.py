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

"""API to interact with the Meraki Dashboard using the requests module."""
import re
import json

import requests
import mechanicalsoup
import bs4


class DataScraper:
    """API to interact with the Meraki Dashboard using the requests module.

    URLs can be generated from org eid and shard id:
    https://n<shard_id>.meraki.com/o/<eid>/manage/organization/

    Attributes:
        username (string): User-entered username, used to login
        password (string): User-entered password, used to login
        browser (MechanicalSoup): Main browser object to send data to dashboard

        vpn_vars (dict): List of VPN variables (does the browser need access
        to this?)

        orgs_dict (dict): A list of orgs/networks derived from administered_orgs
            See method scrape_administered_orgs for more information. Only
            difference from json blob is that network_eid key is replaced
            with network_id key

            = {
                <org#1 id>: {
                    'name'
                    'eid'
                    'node_groups': {
                        <network1_id> : {
                            ...
                        }
                        <network2_id> : {}
                        ...
                    }
                    ...
                }
                <org#2 id>: {}
                ...
            }

        org_qty (int): Number of organizations someone has access to. Once
            determined, it should be invariant.
        active_org_id (int): id of active org.
        active_network_id (int): id of active network.
        is_network_admin (string): If admin has networks but no org access
    """
    def __init__(self):
        super(DataScraper, self).__init__()

        # Instantiate browser
        self.browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},  # Use the lxml HTML parser
            raise_on_404=True,
            # User Agent String is for the Nintendo Switch because why not
            user_agent='Mozilla/5.0 (Nintendo Switch; ShareApplet) '
                       'AppleWebKit/601.6 (KHTML, like Gecko) '
                       'NF/4.0.0.5.9 NintendoBrowser/5.1.0.13341',
        )

        # Setup browser for use by other components
        self.username = ''
        self.password = ''

        # Initialize organization dictionary {Name: Link} and
        # list for easier access. org_list is org_links.keys()
        self.orgs_dict = {}

        self.is_network_admin = False  # Most admins are org admins
        self.org_qty = 1
        self.active_org_id = 0
        self.active_network_id = 0

        # VPN VARS: Powershell Variables set to defaults
        # If it's set to '', then powershell will skip reading that parameter.
        self.vpn_vars = {}

    def attempt_login(self, username, password):
        """Verifies whether credentials are valid

        Uses a MechanicalSoup object to send and submit username/password.
        The resultant URL is different for each auth eventuality and
        is used to identify each.

        Args:
            username (string): The username provided by the user
            password (string): The password provided by the user

        Returns:
            (string): One of ('auth_error', 'sms_auth', 'auth_success')
              indicating the next login step.
        """

        # Set up required vars
        self.username = username
        self.password = password

        # Navigate to login page
        self.browser.open('https://account.meraki.com/login/dashboard_login')
        form = self.browser.select_form()
        self.browser["email"] = self.username
        self.browser["password"] = self.password
        form.choose_submit('commit')  # Click login button
        self.browser.submit_selected()  # response should be '<Response [200]>'
        print("browser url in attempt login " + str(self.browser.get_url()))

        # After setup, verify whether user authenticates correctly
        result_url = self.browser.get_url()
        # URL contains /login/login if login failed

        if '/login/login' in result_url:
            return 'auth_error'
        # Two-Factor redirect: https://account.meraki.com/login/sms_auth?go=%2F
        elif 'sms_auth' in result_url:
            return 'sms_auth'
        else:
            return 'auth_success'

    def tfa_submit_info(self, tfa_code):
        """Attempt login with the provided TFA code.

        Args:
            tfa_code (string): The user-entered TFA string
            (should consist of 6 digits)
        """

        form = self.browser.select_form()
        print(self.browser.get_url())
        self.browser['code'] = tfa_code
        form.choose_submit('commit')  # Click 'Verify' button
        self.browser.submit_selected()

        active_page = self.browser.get_current_page().text
        # Will return -1 if it is not found
        if active_page.find("Invalid verification code") == -1:
            print("TFA Success")
            return True
        else:
            print("TFA Failure")

    def org_data_setup(self):
        """Count whether the admin has access to 0, 1, or 2+ orgs

        This fn will set org qty correctly and add names and urls to org_data.

        NOTE: Don't set data for network-only admins as they don't have
        org-access. Network-only admin data is added in get_networks().

        Set:
            self.org_qty: We should know how many orgs from data on this page
            self.org_data: org names and urls will be added
        """

        print("in fn [count_admin_orgs]")

        # NOTE: Until you choose an organization, Dashboard will not let you
        # visit pages you should have access to
        page = self.browser.get_current_page()
        # 2+ orgs choice page : https://account.meraki.com/login/org_list?go=%2F
        if 'org_list' in self.browser.get_url():  # Admin orgs = 2
            self.bypass_org_choose_page(page)

        administered_orgs = self.scrape_administered_orgs()
        print(administered_orgs)
        # Sort alphabetically by org name
        alphabetized_org_id_list = sorted(
            administered_orgs,
            key=lambda org_id_var: administered_orgs[org_id_var]['name'])
        for org_id in alphabetized_org_id_list:
            # Find active_org_id by finding the name of the org we're in
            if administered_orgs[org_id]['node_groups']:
                self.active_org_id = administered_orgs[org_id]['id']
            # Filter for wired as we only care about firewall networks
            self.orgs_dict[org_id] = self.filter_org_data(
                administered_orgs[org_id],
                ['wired']
            )

        self.active_network_id = list(self.orgs_dict[self.active_org_id][
         'node_groups'])[0]

    def bypass_org_choose_page(self, page):
        """Bypass page for admins with 2+ orgs that normally requires user input

        Admins with 2+ orgs are shown a page where they need to choose an
        organization to enter. This function will follow the link associated
        with the alphabetically first organization and then gather org/network
        info so we have something to show the user.

        Args:
            page (BeautifulSoup): Soup object that we can use to load a link
            to the first org.
        """
        # Get a list of all org links. href comes before a link in HTML.
        org_href_lines = page.findAll(
            'a', href=re.compile('/login/org_choose\?eid=.{6}'))
        # Get the number of orgs
        self.org_qty = len(org_href_lines)
        # Choose link for first org so we have something to connect to
        bootstrap_url = 'https://account.meraki.com' + org_href_lines[0]['href']
        self.browser.open(bootstrap_url)

    @staticmethod
    def get_mkiconf_vars(pagetext):
        """Most dashboard pages have mkiconf vars. This fn returns them.

        These variables are largely the same as administered orgs, but could
        be useful elsewhere. Keeping this here is in case I could use this of
        scraping method later. Check the regex below for the expected string.
        The format will look like this:

            Mkiconf.action_name = "new_wired_status";
            Mkiconf.log_errors = false;
            Mkiconf.eng_log_enabled = false;
            Mkiconf.on_mobile_device = false;

        Essentially  Mkiconf.<property> = <JSON>;

        Args:
            pagetext (string): Text of a webpage

        Returns:
            (dict) All available Mkiconf vars.
        """
        mki_lines = re.findall(' Mkiconf[ -:<-~]*;', pagetext)
        mki_dict = {}
        for line in mki_lines:
            mki_string = re.findall('[0-9a-zA-Z_]+\s*=\s[ -:<-~]*;', line)[0]
            # mki_key = <property>, mki_value = <JSON>
            mki_key, mki_value = mki_string.split(' = ', 1)
            if mki_value[-1] == ';':  # remove trailing ;
                mki_value = mki_value[:-1]
            # If the value is double quoted, remove both "s
            if mki_value[0] == '"' and mki_value[-1] == '"':
                mki_value = mki_value[1:-1]
            mki_dict[mki_key] = mki_value

        return mki_dict

    def scrape_administered_orgs(self):
        """Retrieve the administered_orgs json blob

        For orgs that are not being accessed by the browser, node_groups = {}.
        For this reason, the administered_orgs json needs to be retrieved every
        time the user goes to a different organization.

        * get_networks should only be called on initial startup or if a
          different organization has been chosen
        * browser should have clicked on an org in the org selection page so we
          can browse relative paths of an org

        administered_orgs (dict): A JSON blob provided by /administered_orgs
            that contains useful information about orgs and networks. An eid
            for an org or network is a unique way to refer to it.

            = {
                <org#1 org_id>: {
                    'name' : <org name>
                    'url': <url>,
                    'node_groups': {
                        <network#1 eid> : {
                            'n': <name>
                            'has_wired': <bool>
                            ...
                        }
                        <network#2 eid> : {}
                        ...
                    }
                    ...
                }
                <org#2 org_id>: {}
                ...
            }
        """

        base_url = self.get_url().split('/manage')[0] + '/manage'
        administered_orgs_partial = '/organization/administered_orgs'
        administered_orgs_url = base_url + administered_orgs_partial
        print('administered_orgs url', administered_orgs_url)
        self.browser.open(administered_orgs_url)

        cj = self.browser.get_cookiejar()
        response = requests.get(administered_orgs_url, cookies=cj)
        administered_orgs = json.loads(response.text)
        if self.is_network_admin:
            self.org_qty = len(self.orgs_dict)

        """ For troubleshooting purposes
        print("\nI stole the cookie jar and I put it here:", cj,
              "\nAdministered Orgs =>", json.dumps(administered_orgs,
                                                   indent=4, sort_keys=True))
        """

        return administered_orgs

    @staticmethod
    def filter_org_data(org_dict, network_types):
        """
        Args:
            org_dict (dict): A dict that looks like: administered_orgs[org_id].
            network_types (list): List of strings of target network types

        Returns:
            org_dict (dict): Dict containing all of an org's json except for
            node_groups types not included in network_types

            Also changes network_eid to network_id
        """

        filtered_dict = dict(org_dict)
        # Remove all networks so we can manually add the ones we want
        filtered_dict['node_groups'] = {}

        # eid is alphanumeric id for network
        for eid in org_dict['node_groups']:
            # Only add the network dicts for network types we care about
            eid_dict = org_dict['node_groups'][eid]
            is_filtered_network_type = eid_dict['network_type'] in network_types
            is_templated = eid_dict['is_template_child'] or eid_dict[
                'is_config_template']
            if is_filtered_network_type and not is_templated:
                # Same network ID as in API
                network_id = org_dict['node_groups'][eid]['id']
                filtered_dict['node_groups'][network_id] = \
                    org_dict['node_groups'][eid]

        return filtered_dict

    def scrape_network_vars(self, network_index):
        """Change the current network."""
        print('in scrape network vars. org id',
              self.active_org_id, 'network index', network_index)
        # If this network has not been scraped before
        selected_network_id = list(self.orgs_dict[self.active_org_id][
                                       'node_groups'])[network_index]
        self.active_network_id = selected_network_id
        network_already_scraped = 'psk' in self.orgs_dict[
            self.active_org_id]['node_groups'][self.active_network_id].keys()
        if not network_already_scraped:
            network_dict = self.orgs_dict[self.active_org_id]['node_groups'][
                self.active_network_id]
            network_url_part = network_dict['t'] + '/n/' + network_dict['eid']
            self.scrape_psk(network_url_part)
            self.scrape_ddns_and_ip(network_url_part)

    def scrape_psk(self, network_url_part):
        """Scrape Client VPN PSK"""
        client_vpn_url = self.create_url_from_data(
            network_url_part, '/configure/client_vpn_settings')
        print('Client VPN url', client_vpn_url)
        client_vpn_text = self.browser.get(client_vpn_url).text
        client_vpn_soup = bs4.BeautifulSoup(client_vpn_text, 'lxml')
        psk = client_vpn_soup.find("input", {
            "id": "wired_config_client_vpn_secret", "value": True})['value']
        self.orgs_dict[self.active_org_id]['node_groups'][
            self.active_network_id]['psk'] = psk

    def scrape_ddns_and_ip(self, network_url_part):
        """Scrape the ddns and primary ip address."

        This method gets ddns and ip values for the active network. This
        method should ONLY be called if the user has hit the connect button
        """
        fw_status_url = self.create_url_from_data(
            network_url_part, '/nodes/new_wired_status')
        print('Firewall Status url', fw_status_url)
        fw_status_text = self.browser.get(fw_status_url).text

        # ddns value can be found by searching for '"dynamic_dns_name"'
        ddns_value_start = fw_status_text.find("dynamic_dns_name")+19
        ddns_value_end = fw_status_text[ddns_value_start:].find('\"') \
            + ddns_value_start
        ddns = fw_status_text[ddns_value_start:ddns_value_end]
        self.orgs_dict[self.active_org_id]['node_groups'][
            self.active_network_id]['ddns'] = ddns

        """
        # Primary will always come first, so using find should
        # find it's IP address, even if there's a warm spare
        # Using unique '{"public_ip":' to find primary IP address
        ip_start = fw_status_text.find("{\"public_ip\":")+14
        ip_end = fw_status_text[ip_start:].find('\"') + ip_start
        self.vpn_vars['ip'] = fw_status_text[ip_start: ip_end]
        """

    # Fns that operate independent of which URL the browser is at
    ###########################################################################
    def get_browser(self):
        """Get the MechanicalSoup object with associated login cookies."""
        return self.browser

    def get_url(self):
        """Get the current URL"""
        print("browser url in get_url", self.browser.get_url())
        return self.browser.get_url()

    def get_org_names(self):
        """Get a list of org names"""
        return [self.orgs_dict[org_id]['name'] for org_id in self.orgs_dict]

    # get_active fns get info about the org the browser is at
    ###########################################################################
    def get_active_org_index(self):
        """Return the index of the active org by org_id."""
        return list(self.orgs_dict).index(str(self.active_org_id))

    def set_active_org_index(self, org_index):
        """Set the the org index to the param."""
        self.active_org_id = list(self.orgs_dict)[org_index]
        # If networks have not been retrieved for this org
        if not self.orgs_dict[self.active_org_id]['node_groups']:
            eid = self.orgs_dict[self.active_org_id]['eid']
            new_org_url = self.create_url_from_data('o/' + eid,
                                                    '/organization/')
            self.browser.open(new_org_url)
            new_org_dict = self.scrape_administered_orgs()[self.active_org_id]
            filtered_org_dict = self.filter_org_data(new_org_dict, ['wired'])
            self.orgs_dict[self.active_org_id] = filtered_org_dict

    def create_url_from_data(self, network_partial, url_route):
        """Create the org url from administered_orgs data

        Returns:
            (string): URL that looks like
                https://n<shard_id>.meraki.com/o/<eid>/manage/organization

        NOTE: All names taken from Mkiconf var names in HTML
        """
        shard_id = str(self.orgs_dict[self.active_org_id]['shard_id'])
        shard_origin_url = 'https://n' + shard_id + '.meraki.com/'
        base_url = network_partial + '/manage' + url_route
        return shard_origin_url + base_url

    def get_active_org_name(self):
        """Return the active org name."""
        return self.orgs_dict[self.active_org_id]['name']

    def get_active_org_networks(self):
        """Get the network name for every network in the active org"""
        networks = self.orgs_dict[self.active_org_id]['node_groups']
        print('networks', networks)
        return [networks[network_id]['n'] for network_id in networks]
