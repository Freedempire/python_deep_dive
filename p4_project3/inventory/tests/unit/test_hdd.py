"""
Tests the HDD class
Command line: python -m pytest tests/unit/test_hdd.py
"""

import pytest

from app.models.inventory import HDD

@pytest.fixture
def hdd_values():
    return {
        'name': '1TB SATA HDD',
        'manufacturer': 'Seagate',
        'total': 10,
        'allocated': 3,
        'capacity_GB': 1_000,
        'size': '3.5"',
        'rpm': 10_000
    }

@pytest.fixture
def hdd(hdd_values):
    return HDD(**hdd_values)

def test_create(hdd, hdd_values):
    for attr in hdd_values:
        assert getattr(hdd, attr) == hdd_values.get(attr)

@pytest.mark.parametrize('size, exception',
                         (('2.5', ValueError), ('5.25"', ValueError), (3.5, TypeError)))
def test_create_invalid_size(size, exception, hdd_values):
    hdd_values['size'] = size
    with pytest.raises(exception):
        HDD(**hdd_values)

@pytest.mark.parametrize('rpm, exception',
                         (('100', TypeError), (100, ValueError), (100_000, ValueError)))
def test_create_invalid_rpm(rpm, exception, hdd_values):
    hdd_values['rpm'] = rpm
    with pytest.raises(exception):
        HDD(**hdd_values)
