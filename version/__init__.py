"""
PepeluGPT Version Management Package
"""

from .manager import (
    get_version_info,
    get_age_message,
    get_version_banner,
    get_milestone_history,
    get_version_command_output,
    __version__,
    __codename__,
    __release_date__
)

__all__ = [
    'get_version_info',
    'get_age_message',
    'get_version_banner',
    'get_milestone_history',
    'get_version_command_output',
    '__version__',
    '__codename__',
    '__release_date__'
]
