"""total models"""
from app.utils.validators import validate_integer_arg

class Resource:
    """
    Represents a base class for resources with attributes such as name, manufacturer, total quantity, and allocated quantity.

    Attributes:
        _name (str): The name of the resource.
        _manufacturer (str): The manufacturer of the resource.
        _total (int): The total quantity of the resource.
        _allocated (int): The currently allocated quantity of the resource.
        _variables (list): A list of attribute names used for representation.

    Methods:
        claim(n: int) -> None:
            Claims 'n' units of the resource. Raises an error if no available units.
        free_up(n: int) -> None:
            Frees up 'n' units of the resource. Raises an error if nothing to free.
        remove_died(n: int) -> None:
            Removes 'n' units of the resource. Raises an error if nothing allocated.
        add_purchased(n: int) -> None:
            Adds 'n' units to the total quantity of the resource.
        category() -> str:
            Returns the lowercase class name (category) of the resource.

    Properties:
        name (str): The name of the resource.
        manufacturer (str): The manufacturer of the resource.
        total (int): The total quantity of the resource.
        allocated (int): The currently allocated quantity of the resource.

    Magic Methods:
        __str__() -> str:
            Returns the name of the resource.
        __repr__() -> str:
            Returns a string representation of the resource object.

    Note:
        - The '_set_str_attribute' and '_set_int_attribute' methods are used internally for attribute validation.
        - 'validate_integer_arg' is a util function for integer validation.
    """

    __slots__ = '_name', '_manufacturer', '_total', '_allocated', '_variables'

    def __init__(self, name: str, manufacturer: str, total: int, allocated: int) -> None:
        self._set_str_attribute('_name', name)
        self._set_str_attribute('_manufacturer', manufacturer)
        self._set_int_attribute('_total', total, 0)
        self._set_int_attribute('_allocated', allocated, 0, self._total)
        self._variables = list(locals())[1:]

    def _set_str_attribute(self, attribute_name: str, value: str, allowed: list | tuple=None) -> None:
        if isinstance(value, str):
            if allowed is not None and value not in allowed:
                raise ValueError(f'{attribute_name.removeprefix('_')} must be one of {allowed}')
            setattr(self, attribute_name, value)
        else:
            raise TypeError(f'{attribute_name.removeprefix('_')} must be a str')

    def _set_int_attribute(self, attribute_name: str, value: int, min: int=None, max: int=None) -> None:
        validate_integer_arg(attribute_name.removeprefix('_'), value, min, max)
        setattr(self, attribute_name, value)
        
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def manufacturer(self) -> str:
        return self._manufacturer
    
    @property
    def total(self) -> int:
        return self._total
    
    @property
    def allocated(self) -> int:
        return self._allocated
    
    def __str__(self) -> str:
        return self._name
    
    def __repr__(self) -> str:
        attributes = map(lambda v: f'{v}={getattr(self, v)}', self._variables)
        return f'{self.__class__.__name__}({', '.join(attributes)})'
    
    def claim(self, n: int) -> None:
        available = self._total - self._allocated
        if not available:
            raise RuntimeError('0 available, nothing to claim')
        validate_integer_arg('n', n, 1, available)
        self._allocated += n
    
    def free_up(self, n: int) -> None:
        if self._allocated == 0:
            raise RuntimeError('0 allocated, nothing to free')
        validate_integer_arg('n', n, 1, self._allocated)
        self._allocated -= n
        
    def remove_died(self, n: int) -> None:
        if self._allocated == 0:
            raise RuntimeError('0 allocated, nothing to remove')
        validate_integer_arg('n', n, 1, self._allocated)
        self._allocated -= n
        self._total -= n

    def add_purchased(self, n: int) -> None:
        validate_integer_arg('n', n, 1)
        self._total += n
        
    def category(self) -> str:
        return self.__class__.__name__.lower()
    

class CPU(Resource):
    __slots__ = '_cores', '_socket', '_power_watts'

    def __init__(self, name: str, manufacturer: str, total: int, allocated: int,
                 cores: int, socket: str, power_watts: int) -> None:
        super().__init__(name, manufacturer, total, allocated)
        self.cores = cores
        self.socket = socket
        self.power_watts = power_watts

    @property
    def cores(self) -> int:
        return self._cores
    
    @cores.setter
    def cores(self, cores: int) -> None:
        self._set_int_attribute('_cores', cores, 1)

    @property
    def socket(self) -> str:
        return self._socket
    
    @socket.setter
    def socket(self, socket: str) -> None:
        self._set_str_attribute('_socket', socket)

    @property
    def power_watts(self) -> int:
        return self._power_watts
    
    @power_watts.setter
    def power_watts(self, power_watts: int) -> None:
        self._set_int_attribute('_power_watts', power_watts, 1)


class Storage(Resource):
    __slots__ = '_capacity_GB'

    def __init__(self, name: str, manufacturer: str, total: int, allocated: int,
                 capacity_GB: int) -> None:
        super().__init__(name, manufacturer, total, allocated)
        self.capacity_GB = capacity_GB

    @property
    def capacity_GB(self) -> int:
        return self._capacity_GB
    
    @capacity_GB.setter
    def capacity_GB(self, capacity_GB: int) -> None:
        self._set_int_attribute('_capacity_GB', capacity_GB, 1)


class HDD(Storage):
    __slots__ = '_size', '_rpm'

    def __init__(self, name: str, manufacturer: str, total: int, allocated: int,
                 capacity_GB: int, size: str, rpm: int) -> None:
        super().__init__(name, manufacturer, total, allocated, capacity_GB)
        self.size = size
        self.rpm = rpm

    @property
    def size(self) -> str:
        return self._size
    
    @size.setter
    def size(self, size: str) -> None:
        allowed_sizes = ('2.5"', '3.5"')
        self._set_str_attribute('_size', size, allowed_sizes)

    @property
    def rpm(self) -> int:
        return self._rpm
    
    @rpm.setter
    def rpm(self, rpm: int) -> None:
        self._set_int_attribute('_rpm', rpm, 1000, 50000)


class SSD(Storage):
    __slots__ = '_interface'
    
    def __init__(self, name: str, manufacturer: str, total: int, allocated: int,
                 capacity_GB: int, interface: str) -> None:
        super().__init__(name, manufacturer, total, allocated, capacity_GB)
        self.interface = interface

    @property
    def interface(self) -> str:
        return self._interface
    
    @interface.setter
    def interface(self, interface: str) -> None:
        self._set_str_attribute('_interface', interface)
