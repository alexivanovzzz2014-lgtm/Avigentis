import pytest
from app.core.domain import normalize_domain


def test_normalize_domain_valid():
    assert normalize_domain('https://Example.BG/path') == 'example.bg'


def test_normalize_domain_invalid():
    with pytest.raises(ValueError):
        normalize_domain('http://127.0.0.1/admin')
