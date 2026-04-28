from typing import Set
from urllib.parse import urlparse


def check_url_scheme_and_authority(url: str, allowed_hosts: Set[str]) -> bool:
    """
    Used to prevent open redirects in the flask application. \n
    Allowed arguments:
    - url : The URL string you want to check (full url or authority).
    - allowed_hosts : Set of Strings of hosts you want to allow (with scheme and host and optionally with port).
    """
    if not url:
        return False

    allowed_netloc = set()

    parsed_url_target = urlparse(url)
    scheme_target = parsed_url_target.scheme
    netloc_target = parsed_url_target.netloc

    if not scheme_target and not netloc_target:
        return True

    if (not scheme_target and netloc_target) or (scheme_target and not netloc_target):
        return False

    if scheme_target not in ["http", "https"]:
        return False

    for host in allowed_hosts:
        parsed_url_host = urlparse(host)
        netloc_host = parsed_url_host.netloc
        allowed_netloc.add(netloc_host) if netloc_host else allowed_netloc.add(host)

    return netloc_target in allowed_netloc