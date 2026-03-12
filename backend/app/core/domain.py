import re
from urllib.parse import urlparse

DOMAIN_RE = re.compile(r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,63}$')


def normalize_domain(raw: str) -> str:
    candidate = raw.strip().lower()
    if '://' in candidate:
        parsed = urlparse(candidate)
        candidate = parsed.netloc
    candidate = candidate.split('/')[0].split(':')[0].strip('.')
    if not DOMAIN_RE.match(candidate):
        raise ValueError('Invalid domain. Provide a domain only, no paths or query params.')
    return candidate
