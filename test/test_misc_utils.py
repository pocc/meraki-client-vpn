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
import merlink.os_utils
import merlink.browsers.pages.page_hunters
import merlink.browsers.pages.page_utils


class TestMiscUtils(unittest.TestCase):
    """Test the dashboard browser class."""

    @staticmethod
    def set_up():
        """Set up the test."""
        pass

    @staticmethod
    def test_a_fn():
        """Test these functions... eventually.
        os_utils
            kill_duplicate_applications
            is_online
            list_vpns
            open_vpn_settings
            pyinstaller_path
        page_hunters
            get_pagetext_json_value
            get_pagetext_mkiconf
            get_pagetext_links
        page_utils
            get_textarea_list
            get_dropdown_value
            get_all_dropdown_values
            get_input_var_value
            save_page
        """


if __name__ == '__main__':
    unittest.main()



