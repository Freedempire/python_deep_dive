"""
Tests the CPU class
Command line: python -m pytest tests/unit/test_cpu.py
"""

import pytest

from app.models.inventory import CPU

@pytest.fixture
def cpu_values():
    return {
        'name': 'RYZEN Threadripper 2990WX',
        'manufacturer': 'AMD',
        'total': 10,
        'allocated': 3,
        'cores': 32,
        'socket': 'sTR4',
        'power_watts': 250
    }

@pytest.fixture
def cpu(cpu_values):
    return CPU(**cpu_values)

def test_create_cpu(cpu, cpu_values):
    for attr in cpu_values:
        assert getattr(cpu, attr) == cpu_values.get(attr)

@pytest.mark.parametrize('cores, exception',
                         ((10.5, TypeError), (-1, ValueError), (0, ValueError)))
def test_create_invalid_cores(cores, exception, cpu_values):
    cpu_values['cores'] = cores
    with pytest.raises(exception):
        CPU(**cpu_values)

@pytest.mark.parametrize('watts, exception',
                         (('10.5', TypeError), (-1, ValueError), (0, ValueError)))
def test_create_invalid_power(watts, exception, cpu_values):
    cpu_values['power_watts'] = watts
    with pytest.raises(exception):
        CPU(**cpu_values)
