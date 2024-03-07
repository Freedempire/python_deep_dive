"""
Tests the Resource class
Command line: python -m pytest tests/unit/test_resource.py
"""
# Under the root directory of the project (where the tests folder is located),
# use `python -m pytest` will automatically discover and execute all tests in
# files whose names follow the form `test_*.py` or `*_test.py` within the
# current directory and its subdirectories
# To see more detailed output, use: `pytest --verbose --capture=no`

import pytest

from app.models.inventory import Resource

@pytest.fixture
def resource_values():
    return {'name': 'Sample Resource', 'manufacturer': 'ABC Corp',
            'total': 100, 'allocated': 20}

@pytest.fixture
def resource(resource_values):
    return Resource(**resource_values)

# Test initialization
def test_resource_initialization(resource, resource_values):
    # assert resource.name == resource_values['name']
    # assert resource.manufacturer == resource_values['manufacturer']
    # assert resource.total == resource_values['total']
    # assert resource.allocated == resource_values['allocated']
    for attr in resource_values:
        assert getattr(resource, attr) == resource_values.get(attr)

@pytest.mark.parametrize('total, allocated', ((10, 20), (-10, 0), (0, -10), ('10', 1), (10, '1')))
def test_resource_initialization_invalid(total, allocated):
    with pytest.raises((ValueError, TypeError)):
        Resource('name', 'manufacturer', total, allocated)

# Test claim method
def test_claim(resource, resource_values):
    resource.claim(10)
    assert resource.allocated == resource_values['allocated'] + 10

    # Test claiming more than available
    with pytest.raises(ValueError, match=f'cannot be greater than'):
        resource.claim(1000)

    # Test claiming less than 1
    with pytest.raises(ValueError, match=f'cannot be less than'):
        resource.claim(0)

    # Test claiming with 0 available
    resource.claim(resource.total - resource.allocated)
    with pytest.raises(RuntimeError, match=f'nothing to claim'):
        resource.claim(1)

# Test free_up method
def test_free_up(resource, resource_values):
    resource.free_up(5)
    assert resource.allocated == resource_values['allocated'] - 5

    # Test freeing up more than allocated
    with pytest.raises(ValueError, match="cannot be greater than"):
        resource.free_up(resource.allocated + 1)

    # Test freeing up less than 1
    with pytest.raises(ValueError, match="cannot be less than"):
        resource.free_up(-1)

    # Test freeing up with 0 allocated
    resource.free_up(resource.allocated)
    with pytest.raises(RuntimeError, match="nothing to free"):
        resource.free_up(1)

# Test remove_died method
def test_remove_died(resource, resource_values):
    resource.remove_died(10)
    assert resource.allocated == resource_values['allocated'] - 10
    assert resource.total == resource_values['total'] - 10

    # Test removing more than allocated
    with pytest.raises(ValueError, match="cannot be greater than"):
        resource.remove_died(resource.allocated + 1)

    # Test removing less than 1
    with pytest.raises(ValueError, match="cannot be less than"):
        resource.remove_died(-1)

    # Test removing with 0 allocated
    resource.free_up(resource.allocated)
    with pytest.raises(RuntimeError, match="nothing to remove"):
        resource.remove_died(1)
    
# Test category method
def test_category(resource):
    assert resource.category() == 'resource'

# if __name__ == '__main__':
#     pytest.main()
