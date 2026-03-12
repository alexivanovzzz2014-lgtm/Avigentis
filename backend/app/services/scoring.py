SCORING_WEIGHTS = {
    'no_https': 30,
    'invalid_ssl': 25,
    'no_http_redirect': 10,
    'no_dmarc': 12,
    'no_spf': 10,
    'missing_header': 5,
    'no_privacy_policy': 6,
    'no_cookie_policy': 4,
    'server_leakage': 4,
}


def compute_score(results: dict) -> tuple[float, str, list[str]]:
    score = 100
    penalties: list[str] = []

    https = results['https_ssl']
    if https['https_available']['status'] == 'fail':
        score -= SCORING_WEIGHTS['no_https']
        penalties.append('HTTPS not publicly reachable')
    if https['certificate'].get('status') == 'fail':
        score -= SCORING_WEIGHTS['invalid_ssl']
        penalties.append('SSL certificate appears invalid or expired')

    if results['http_redirect']['status'] == 'fail':
        score -= SCORING_WEIGHTS['no_http_redirect']
        penalties.append('HTTP to HTTPS redirect missing')

    dns = results['dns_email']
    if dns['dmarc']['status'] == 'fail':
        score -= SCORING_WEIGHTS['no_dmarc']
        penalties.append('DMARC record not found')
    if dns['spf']['status'] == 'fail':
        score -= SCORING_WEIGHTS['no_spf']
        penalties.append('SPF record not found')

    for hdr in results['security_headers'].values():
        if hdr['status'] == 'fail':
            score -= SCORING_WEIGHTS['missing_header']

    governance = results['governance']
    if governance['privacy_policy']['status'] == 'fail':
        score -= SCORING_WEIGHTS['no_privacy_policy']
        penalties.append('Privacy policy signal not found')
    if governance['cookie_policy']['status'] == 'fail':
        score -= SCORING_WEIGHTS['no_cookie_policy']
        penalties.append('Cookie policy signal not found')
    if governance['server_leakage']['status'] == 'fail':
        score -= SCORING_WEIGHTS['server_leakage']
        penalties.append('Server technology leakage visible')

    score = max(0, min(100, score))
    if score <= 30:
        status = 'High priority for expert review'
    elif score <= 60:
        status = 'Medium readiness'
    elif score <= 80:
        status = 'Basic cyber hygiene present'
    else:
        status = 'Good public signals, expert verification recommended'
    return score, status, penalties
