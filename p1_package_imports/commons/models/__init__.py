from .posts import *
from .users import *

# only take effect when the module is imported with *
__all__ = posts.__all__ + users.__all__
