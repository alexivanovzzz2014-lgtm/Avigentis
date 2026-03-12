from app.services.summary import generate_internal_summary, generate_public_summary


def test_public_summary_contains_disclaimer():
    text = generate_public_summary('example.bg', 55, 'Medium readiness', ['DMARC record not found'])
    assert 'публично достъпна информация' in text
    assert 'preliminary' in text.lower()


def test_internal_summary_contains_package():
    text = generate_internal_summary('example.bg', 20, 'High priority for expert review', ['HTTPS not publicly reachable'], {})
    assert 'Full package' in text
