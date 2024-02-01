# defines a list of names to be imported when imported with *
__all__ = ['is_numeric']

def is_integer():
    pass

def is_numeric():
    pass

# the starting _ excludes the function being imported when imported with *
def _numeric_helper():
    pass
