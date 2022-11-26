import email
from slowapi import Limiter
from slowapi.util import get_remote_address
from pkg_resources import get_distribution

__name__ = get_distribution("backend").project_name
__version__ = get_distribution("backend").version
__description__ = email.message_from_string(get_distribution("backend").get_metadata('PKG-INFO'))['Summary']

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
