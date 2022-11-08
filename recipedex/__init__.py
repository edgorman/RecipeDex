import email
from pkg_resources import get_distribution

from recipedex.app import App


__name__ = get_distribution("recipedex").project_name
__version__ = get_distribution("recipedex").version
__description__ = email.message_from_string(get_distribution("recipedex").get_metadata('PKG-INFO'))['Summary']
