def validate_integer_arg(arg_name: str, arg_value: int, min_value: int=None,
                         max_value: int=None) -> None:
    """
    Validates an integer argument based on optional minimum and maximum values.

    Args:
        arg_name (str): The name of the argument being validated.
        arg_value (int): The value of the argument to be validated.
        min_value (int, optional): Minimum allowed value (inclusive). Defaults to None.
        max_value (int, optional): Maximum allowed value (inclusive). Defaults to None.

    Raises:
        TypeError: If the argument value is not an integer.
        ValueError: If the argument value is outside the specified range.

    Example:
        validate_integer_arg('age', 25, min_value=18, max_value=100)
        # Validates that 'age' is an integer between 18 and 100 (inclusive).
    """
    if not isinstance(arg_value, int):
        raise TypeError(f'{arg_name} must be an int')
    if min_value is not None and arg_value < min_value:
        raise ValueError(f'{arg_name} cannot be less than {min_value}')
    if max_value is not None and arg_value > max_value:
        raise ValueError(f'{arg_name} cannot be greater than {max_value}')