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
"""Test dashboard browser class."""
import unittest
from merlink.browsers.dashboard import DashboardBrowser


class TestDashboardBrowser(unittest.TestCase):
    """Test the dashboard browser class."""

    @staticmethod
    def set_up():
        """Set up the test."""
        pass

    @staticmethod
    def test_a_fn():
        """Test these functions... eventually.
        'bypass_org_choose_page', 
        'combined_network_redirect', 
        'get_active_network_name', 
        'get_active_org_name',
        'get_network_names',
        'get_org_names',
        'handle_redirects',
        'login', 
        'logout', 
        'open_route', 
        'org_data_setup', 
        'scrape_json', 
        'set_network_id', 
        'set_network_name', 
        'set_org_id', 
        'set_org_name', 
        'tfa_submit_info', 
        'url'
        """

        browser = DashboardBrowser()
        browser.org_data_setup()


if __name__ == '__main__':
    unittest.main()

