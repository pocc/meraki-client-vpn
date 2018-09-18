# -*- coding: utf-8 -*-
"""Add additional functions to dashboard_browser.py from pages/."""
from .pages.mr import mr_get_group_policies_by_device_type_enabled
from .pages.mr import mr_get_ssids

from .pages.ms import ms_get_management_vlan
from .pages.ms import ms_get_rstp_enabled

from .pages.mx import mx_get_client_vpn_subnet
from .pages.mx import mx_get_client_vpn_dns_mode
from .pages.mx import mx_get_client_vpn_nameservers
from .pages.mx import mx_get_client_vpn_wins_enabled
from .pages.mx import mx_get_client_vpn_secret
from .pages.mx import mx_get_client_auth_type
from .pages.mx import mx_get_sentry_vpn_enabled
from .pages.mx import mx_get_active_directory_enabled
from .pages.mx import mx_get_primary_uplink
from .pages.mx import mx_get_amp_enabled
from .pages.mx import mx_get_ids_mode
from .pages.mx import mx_get_ids_ruleset

from .pages.json_hunters import scrape_administered_orgs
from .pages.json_hunters import get_json_value
from .pages.json_hunters import get_mkiconf_vars
from .pages.json_hunters import get_network_users
from .pages.json_hunters import get_node_settings_json
from .pages.json_hunters import get_page_links
from .pages.json_hunters import handle_redirects
from .pages.json_hunters import open_route
from .pages.json_hunters import combined_network_redirect


def add_functions_as_methods(functions):
    """docstring."""
    def decorator(this_class):
        """docstring."""
        for func in functions:
            setattr(this_class, func.__name__, func)
        return this_class
    return decorator


page_scrapers = [
    mr_get_group_policies_by_device_type_enabled,
    mr_get_ssids,

    ms_get_management_vlan,
    ms_get_rstp_enabled,

    mx_get_client_vpn_subnet,
    mx_get_client_vpn_dns_mode,
    mx_get_client_vpn_nameservers,
    mx_get_client_vpn_wins_enabled,
    mx_get_client_vpn_secret,
    mx_get_client_auth_type,
    mx_get_sentry_vpn_enabled,
    mx_get_active_directory_enabled,
    mx_get_primary_uplink,
    mx_get_amp_enabled,
    mx_get_ids_mode,
    mx_get_ids_ruleset,

    # JSON hunters
    scrape_administered_orgs,
    get_json_value,
    get_mkiconf_vars,
    get_network_users,
    get_node_settings_json,
    get_page_links,
    open_route,
    combined_network_redirect,
    handle_redirects,
]
