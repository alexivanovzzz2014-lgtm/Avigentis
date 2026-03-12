import re
import socket
import ssl
from datetime import datetime

import dns.resolver
import httpx

TIMEOUT = httpx.Timeout(6.0)
HEADERS_TO_CHECK = [
    'strict-transport-security',
    'content-security-policy',
    'x-frame-options',
    'x-content-type-options',
    'referrer-policy',
]


def _unknown(explanation: str = 'insufficient public evidence') -> dict:
    return {'status': 'unknown', 'explanation': explanation}


def check_https_and_ssl(domain: str) -> dict:
    result = {'https_available': _unknown(), 'certificate': _unknown(), 'tls_handshake': _unknown()}
    try:
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ssl.create_default_context().wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                result['https_available'] = {'status': 'pass', 'explanation': 'HTTPS endpoint responded'}
                result['tls_handshake'] = {'status': 'pass', 'explanation': 'TLS handshake successful'}
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                result['certificate'] = {
                    'status': 'pass' if not_after > datetime.utcnow() else 'fail',
                    'expires_at': not_after.isoformat(),
                    'explanation': 'Certificate expiration evaluated from public certificate metadata.',
                }
    except Exception:
        result['https_available'] = {'status': 'fail', 'explanation': 'HTTPS not publicly reachable'}
        result['tls_handshake'] = {'status': 'fail', 'explanation': 'TLS handshake failed'}
    return result


def check_http_redirect(domain: str) -> dict:
    try:
        with httpx.Client(timeout=TIMEOUT, follow_redirects=False) as client:
            response = client.get(f'http://{domain}')
        location = response.headers.get('location', '')
        if response.status_code in (301, 302, 307, 308) and location.startswith('https://'):
            return {'status': 'pass', 'explanation': 'HTTP redirects to HTTPS'}
        return {'status': 'fail', 'explanation': 'No clear redirect from HTTP to HTTPS'}
    except Exception:
        return _unknown()


def check_security_headers(domain: str) -> dict:
    try:
        response = httpx.get(f'https://{domain}', timeout=TIMEOUT, follow_redirects=True)
    except Exception:
        return {h: _unknown() for h in HEADERS_TO_CHECK}
    output = {}
    for header in HEADERS_TO_CHECK:
        output[header] = {
            'status': 'pass' if header in response.headers else 'fail',
            'explanation': 'Header visible in public response.' if header in response.headers else 'Header not found in public response.',
        }
    return output


def check_dns_records(domain: str) -> dict:
    resolver = dns.resolver.Resolver()
    result = {'mx': _unknown(), 'spf': _unknown(), 'dmarc': _unknown(), 'dkim': _unknown()}

    try:
        mx = resolver.resolve(domain, 'MX')
        result['mx'] = {'status': 'pass', 'values': [str(r.exchange) for r in mx], 'explanation': 'Public MX records found.'}
    except Exception:
        result['mx'] = {'status': 'fail', 'explanation': 'No public MX records found.'}

    try:
        txt = resolver.resolve(domain, 'TXT')
        texts = [''.join(t.decode() for t in r.strings) for r in txt]
        has_spf = any('v=spf1' in t.lower() for t in texts)
        result['spf'] = {'status': 'pass' if has_spf else 'fail', 'explanation': 'SPF TXT present.' if has_spf else 'SPF TXT not found.'}
    except Exception:
        result['spf'] = _unknown()

    try:
        dmarc = resolver.resolve(f'_dmarc.{domain}', 'TXT')
        texts = [''.join(t.decode() for t in r.strings) for r in dmarc]
        has_dmarc = any('v=dmarc1' in t.lower() for t in texts)
        result['dmarc'] = {'status': 'pass' if has_dmarc else 'fail', 'explanation': 'DMARC TXT present.' if has_dmarc else 'DMARC TXT not found.'}
    except Exception:
        result['dmarc'] = {'status': 'fail', 'explanation': 'DMARC TXT not found.'}

    selectors = ['default', 'selector1', 'selector2', 'google']
    found = False
    for selector in selectors:
        try:
            resolver.resolve(f'{selector}._domainkey.{domain}', 'TXT')
            found = True
            break
        except Exception:
            continue
    result['dkim'] = {'status': 'pass', 'explanation': 'DKIM selector discovered publicly.'} if found else _unknown()
    return result


def governance_checks(domain: str) -> dict:
    results = {
        'cookie_policy': _unknown(),
        'privacy_policy': _unknown(),
        'robots_txt': _unknown(),
        'security_txt': _unknown(),
        'mixed_content': _unknown(),
        'cms_fingerprint': _unknown(),
        'server_leakage': _unknown(),
    }
    try:
        response = httpx.get(f'https://{domain}', timeout=TIMEOUT, follow_redirects=True)
        html = response.text.lower()
        results['cookie_policy'] = {'status': 'pass' if 'cookie' in html else 'fail', 'explanation': 'Keyword-based presence check.'}
        results['privacy_policy'] = {'status': 'pass' if 'privacy' in html or 'поверителност' in html else 'fail', 'explanation': 'Keyword-based presence check.'}
        results['mixed_content'] = {'status': 'fail' if re.search(r'http://', html) else 'pass', 'explanation': 'Basic static reference check for http:// resources.'}
        server = response.headers.get('server')
        powered = response.headers.get('x-powered-by')
        leakage = ', '.join([x for x in [server, powered] if x])
        results['server_leakage'] = {'status': 'fail' if leakage else 'pass', 'explanation': f'Visible technology headers: {leakage}' if leakage else 'No obvious server leakage headers.'}

        if 'wp-content' in html:
            results['cms_fingerprint'] = {'status': 'pass', 'value': 'WordPress', 'explanation': 'Public CMS marker detected.'}
        elif 'drupal' in html:
            results['cms_fingerprint'] = {'status': 'pass', 'value': 'Drupal', 'explanation': 'Public CMS marker detected.'}
        else:
            results['cms_fingerprint'] = _unknown()
    except Exception:
        pass

    for endpoint, key in [('/robots.txt', 'robots_txt'), ('/.well-known/security.txt', 'security_txt')]:
        try:
            r = httpx.get(f'https://{domain}{endpoint}', timeout=TIMEOUT)
            results[key] = {'status': 'pass' if r.status_code == 200 else 'fail', 'explanation': 'Public file check.'}
        except Exception:
            results[key] = _unknown()
    return results


def run_scan(domain: str) -> dict:
    return {
        'https_ssl': check_https_and_ssl(domain),
        'http_redirect': check_http_redirect(domain),
        'security_headers': check_security_headers(domain),
        'dns_email': check_dns_records(domain),
        'governance': governance_checks(domain),
        'methodology': {
            'scope': 'publicly visible indicators only',
            'limitations': 'not a pentest, not a formal audit, not a legal opinion',
        },
    }
