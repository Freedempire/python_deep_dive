"""
Tests the validator functions
Command line: python -m pytest tests/test_validators.py
"""

import pytest

from app.utils.validators import validate_integer_arg

class TestIntegerValidator:
    def test_valid_integer(self):
        # Test with a valid integer value
        validate_integer_arg("age", 25, min_value=18, max_value=100)

    def test_invalid_integer_type(self):
        # Test with a non-integer value
        with pytest.raises(TypeError, match="must be an int"):
            validate_integer_arg("height", "not_an_integer")

    def test_integer_below_min_value(self):
        # Test with an integer below the specified minimum value
        with pytest.raises(ValueError, match="cannot be less than 10"):
            validate_integer_arg("score", 5, min_value=10)

    def test_integer_above_max_value(self):
        # Test with an integer above the specified maximum value
        with pytest.raises(ValueError, match="cannot be greater than 100"):
            validate_integer_arg("temperature", 110, max_value=100)

    def test_no_min_max_values(self):
        # Test without specifying min_value and max_value
        validate_integer_arg("quantity", 42)  # No exceptions should be raised
