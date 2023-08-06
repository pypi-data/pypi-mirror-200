"""
plugin_registery.py
===================
The core module for registering plugins.
"""

from nsaphx.plugins.filter import filter

PLUGIN_MAP = {
    "filter": filter.filter_plugin,
    "drop_na": filter.drop_na
}