import pytest

fastapi = pytest.importorskip('fastapi')
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_scan_creation_flow():
    payload = {
        'domain': 'example.bg',
        'email': 'lead@example.bg',
        'gdpr_consent': True,
        'public_info_acknowledgment': True,
        'organization_type': 'Municipality',
    }
    response = client.post('/api/scans', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['normalized_domain'] == 'example.bg'
    assert 'preliminary' in data['public_summary'].lower()
