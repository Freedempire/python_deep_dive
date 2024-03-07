class Resource:
    __slots__ = '_name', '_manufacturer', '_inventory', '_allocated', '_variables'

    def __init__(self, name, manufacturer, inventory, allocated):
        # self.name = name
        # self.manufacturer = manufacturer
        # self.inventory = inventory
        # self.allocated = allocated

        # make properties read-only
        self._set_str_attribute('_name', name)
        self._set_str_attribute('_manufacturer', manufacturer)
        self._set_int_attribute('_inventory', inventory)
        self._set_int_attribute('_allocated', allocated)
        self._variables = list(locals())[1:]

    def _set_str_attribute(self, attribute_name, value):
        if isinstance(value, str):
            setattr(self, attribute_name, value)
        else:
            raise TypeError(f'{attribute_name.removeprefix('_')} should be a str')

    def _set_int_attribute(self, attribute_name, value, min=0, max=None):
        if not isinstance(value, int):
            raise TypeError(f'{attribute_name.removeprefix('_')} should be an int')
        
        if min is not None and value < min:
            raise ValueError(f'{attribute_name.removeprefix('_')} should be an int no less than {min}')

        if max is not None and value > max:
            raise ValueError(f'{attribute_name.removeprefix('_')} should be an int no greater than {max}')

        setattr(self, attribute_name, value)
        
    @property
    def name(self):
        return self._name
    
    # @name.setter
    # def name(self, name):
    #     self._set_str_attribute('_name', name)
    
    @property
    def manufacturer(self):
        return self._manufacturer
    
    # @manufacturer.setter
    # def manufacturer(self, manufacturer):
    #     self._set_str_attribute('_manufacturer', manufacturer)
    
    @property
    def inventory(self):
        return self._inventory
    
    # @inventory.setter
    # def inventory(self, inventory):
    #     self._set_int_attribute('_inventory', inventory)
    
    @property
    def allocated(self):
        return self._allocated
    
    # @allocated.setter
    # def allocated(self, allocated):
    #     self._set_int_attribute('_allocated', allocated)
        
    def __str__(self):
        return self._name
    
    def __repr__(self):
        attributes = map(lambda v: f'{v}={getattr(self, v)}', self._variables)
        return f'{self.__class__.__name__}({', '.join(attributes)})'
    
    def claim(self, n):
        if isinstance(n, int) and 0 < n <= self._inventory:
            self._inventory -= n
            self._allocated += n
        else:
            raise ValueError('n should be a positive integer no greater than inventory')
    
    def free_up(self, n):
        if self._allocated == 0:
            raise RuntimeError('0 allocated, nothing to free up')
        if isinstance(n, int) and 0 < n <= self._allocated:
            self._allocated -= n
            self._inventory += n
        else:
            raise ValueError('n should be a positive integer no greater than allocated')
        
    def remove_died(self, n):
        if self._inventory == 0:
            raise RuntimeError('0 inventory, nothing to remove')
        if isinstance(n, int) and 0 < n <= self._inventory:
            self._inventory -= n
        else:
            raise ValueError('n should be a positive integer no greater than inventory')

    def add_purchased(self, n):
        if isinstance(n, int) and n > 0:
            self._inventory += n
        else:
            raise ValueError('n should be a positive integer')
        
    def category(self):
        return self.__class__.__name__.lower()
    

class CPU(Resource):
    __slots__ = '_cores', '_socket', '_power_watts'

    def __init__(self, name, manufacturer, inventory, allocated, cores, socket, power_watts):
        super().__init__(name, manufacturer, inventory, allocated)
        self.cores = cores
        self.socket = socket
        self.power_watts = power_watts

    @property
    def cores(self):
        return self._cores
    
    @cores.setter
    def cores(self, cores):
        self._set_int_attribute('_cores', cores, 1)

    @property
    def socket(self):
        return self._socket
    
    @socket.setter
    def socket(self, socket):
        self._set_str_attribute('_socket', socket)

    @property
    def power_watts(self):
        return self._power_watts
    
    @power_watts.setter
    def power_watts(self, power_watts):
        self._set_int_attribute('_power_watts', power_watts, 1)


class Storage(Resource):
    __slots__ = '_capacity_GB'

    def __init__(self, name, manufacturer, inventory, allocated, capacity_GB):
        super().__init__(name, manufacturer, inventory, allocated)
        self.capacity_GB = capacity_GB

    @property
    def capacity_GB(self):
        return self._capacity_GB
    
    @capacity_GB.setter
    def capacity_GB(self, capacity_GB):
        self._set_int_attribute('_capacity_GB', capacity_GB, 1)


class HDD(Storage):
    __slots__ = '_size', '_rpm'

    def __init__(self, name, manufacturer, inventory, allocated, capacity_GB, size, rpm):
        super().__init__(name, manufacturer, inventory, allocated, capacity_GB)
        self.size = size
        self.rpm = rpm

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size):
        self._set_str_attribute('_size', size)

    @property
    def rpm(self):
        return self._rpm
    
    @rpm.setter
    def rpm(self, rpm):
        self._set_int_attribute('_rpm', rpm, 1)


class SSD(Storage):
    __slots__ = '_interface'
    
    def __init__(self, name, manufacturer, inventory, allocated, capacity_GB, interface):
        super().__init__(name, manufacturer, inventory, allocated, capacity_GB)
        self.interface = interface

    @property
    def interface(self):
        return self._interface
    
    @interface.setter
    def interface(self, interface):
        self._set_str_attribute('_interface', interface)
