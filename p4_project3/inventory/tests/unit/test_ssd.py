"""
Tests the SSD class
Command line: python -m pytest tests/unit/test_ssd.py
"""

import pytest

from app.models.inventory import SSD

@pytest.fixture
def ssd_values():
    return {
        'name': 'Samsung 860 EVO',
        'manufacturer': 'Samsung',
        'total': 10,
        'allocated': 3,
        'capacity_GB': 1_000,
        'interface': 'SATA III'
    }

@pytest.fixture
def ssd(ssd_values):
    return SSD(**ssd_values)

def test_create(ssd, ssd_values):
    for attr in ssd_values:
        assert getattr(ssd, attr) == ssd_values.get(attr)
