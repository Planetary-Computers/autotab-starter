from urllib.parse import urlparse


def extract_domain_from_url(url: str):
    # url = http://username:password@hostname:port/path?arg=value#anchor
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    if hostname is None:
        raise ValueError(f"Could not extract hostname from url {url}")
    if hostname.startswith("www."):
        hostname = hostname[4:]
    return hostname
