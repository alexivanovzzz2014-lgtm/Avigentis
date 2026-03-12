from app.services.scoring import compute_score


def _base_results():
    return {
        'https_ssl': {'https_available': {'status': 'pass'}, 'certificate': {'status': 'pass'}},
        'http_redirect': {'status': 'pass'},
        'dns_email': {'dmarc': {'status': 'pass'}, 'spf': {'status': 'pass'}},
        'security_headers': {f'h{i}': {'status': 'pass'} for i in range(5)},
        'governance': {'privacy_policy': {'status': 'pass'}, 'cookie_policy': {'status': 'pass'}, 'server_leakage': {'status': 'pass'}},
    }


def test_scoring_good_band():
    score, status, _ = compute_score(_base_results())
    assert score == 100
    assert 'Good public signals' in status


def test_scoring_penalties_applied():
    r = _base_results()
    r['https_ssl']['https_available']['status'] = 'fail'
    r['dns_email']['dmarc']['status'] = 'fail'
    score, status, penalties = compute_score(r)
    assert score < 70
    assert penalties
    assert status in ['Medium readiness', 'High priority for expert review']
