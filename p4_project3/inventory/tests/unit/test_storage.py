"""
Tests the Storage class
Command line: python -m pytest tests/unit/test_storage.py
"""

import pytest

from app.models.inventory import Storage

@pytest.fixture
def storage_values():
    return {
        'name': 'Thumbdrive',
        'manufacturer': 'Sandisk',
        'total': 10,
        'allocated': 3,
        'capacity_GB': 512
    }

@pytest.fixture
def storage(storage_values):
    return Storage(**storage_values)

def test_create(storage, storage_values):
    for attr in storage_values:
        assert getattr(storage, attr) == storage_values.get(attr)

@pytest.mark.parametrize('capacity_GB, exception',
                         ((10.5, TypeError), ('10.5', TypeError), (-1, ValueError), (0, ValueError)))
def test_create_invalid_storage(capacity_GB, exception, storage_values):
    storage_values['capacity_GB'] = capacity_GB
    with pytest.raises(exception):
        Storage(**storage_values)
