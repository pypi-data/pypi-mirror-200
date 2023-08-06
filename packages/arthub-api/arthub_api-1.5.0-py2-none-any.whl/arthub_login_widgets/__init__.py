"""A Qt Widget for login ArtHub."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import third-party modules
# Disabling the import error because PyLint chokes on importing pkg_resources,
# it is available though.
# pylint: disable=import-error
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # Package is not installed
    __version__ = "0.0.0-dev.1"

# Import local modules
from arthub_login_widgets.core import LoginWindow
from arthub_login_widgets.filesystem import get_login_account

# All public APis
__all__ = ["LoginWindow", "get_login_account"]
