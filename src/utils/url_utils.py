from urllib.parse import urlparse

def clean_url(url: str):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc or parsed_url.path
    domain = domain.split(":")[0]
    domain = domain.split("@")[-1]
    domain = domain.split(".")
    domain = ".".join(domain[-2:])
    return domain