from functools import total_ordering

@total_ordering
class Mod:
    def __init__(self, value, modulus):
        self._set_modulus(modulus)
        self._set_value(value)

    @property
    def value(self):
        return self._value
    
    @property
    def modulus(self):
        return self._modulus
    
    def _set_modulus(self, modulus):
        if not isinstance(modulus, int):
            raise TypeError('modulus should be of int type')
        if modulus <= 0:
            raise ValueError('modulus should be positive')
        self._modulus = modulus

    def _set_value(self, value):
        if not isinstance(value, int):
            raise TypeError('value should be of int type')
        self._value = value % self.modulus

    def __repr__(self):
        return f'Mod(value={self._value}, modulus={self._modulus})'
    
    def __lt__(self, other):
        if isinstance(other, int):
            return self._value < other % self._modulus
        if isinstance(other, Mod):
            if self._modulus == other._modulus:
                return self._value < other._value
            else:
                return ValueError('comparison unsupported between Mod instances with different moduli')
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, int):
            return self._value == other % self._modulus
        if isinstance(other, Mod):
            if self._modulus == other._modulus:
                return self._value == other._value
            else:
                raise ValueError('comparison unsupported between Mod instances with different moduli')
        return NotImplemented
    
    def __hash__(self):
        return hash((self._value, self._modulus))
    
    def __int__(self):
        return self._value
    
    def __neg__(self):
        return Mod(-self._value, self._modulus)
    
    def __add__(self, other):
        if isinstance(other, int):
            return Mod(self._value + other, self._modulus)
        if isinstance(other, Mod):
            if self._modulus == other._modulus:
                return Mod(self._value + other._value, self._modulus)
            else:
                raise ValueError('operands should have same modulus')
        raise TypeError(f'unsupported operand type(s) for +: \'Mod\' and {type(other).__name__!r}')
        # return NotImplemented

    def __sub__(self, other):
        if isinstance(other, int):
            return Mod(self._value - other, self._modulus)
        if isinstance(other, Mod):
            if self._modulus == other._modulus:
                return Mod(self._value - other._value, self._modulus)
            else:
                raise ValueError('operands should have same modulus')
        raise TypeError(f'unsupported operand type(s) for +: \'Mod\' and {type(other).__name__!r}')

    def __mul__(self, other):
        if isinstance(other, int):
            return Mod(self._value * other, self._modulus)
        if isinstance(other, Mod):
            if self._modulus == other._modulus:
                return Mod(self._value * other._value, self._modulus)
            else:
                raise ValueError('operands should have same modulus')
        raise TypeError(f'unsupported operand type(s) for +: \'Mod\' and {type(other).__name__!r}')

    def __pow__(self, other):
        if isinstance(other, int):
            return Mod(self._value ** other, self._modulus)
        if isinstance(other, Mod):
            if self._modulus == other._modulus:
                return Mod(self._value ** other._value, self._modulus)
            else:
                raise ValueError('operands should have same modulus')
        raise TypeError(f'unsupported operand type(s) for +: \'Mod\' and {type(other).__name__!r}')

    def __iadd__(self, other):
        if isinstance(other, int):
            # self._value = (self._value + other) % self._modulus
            self._set_value(self._value + other)
            return self
        if isinstance(other, Mod):
            if self._modulus == other._modulus:
                self._set_value(self._value + other._value)
                return self
            else:
                raise ValueError('operands should have same modulus')
        raise TypeError(f'unsupported operand type(s) for +: \'Mod\' and {type(other).__name__!r}')

    def __isub__(self, other):
        if isinstance(other, int):
            self._set_value(self._value - other)
            return self
        if isinstance(other, Mod):
            if self._modulus == other._modulus:
                self._set_value(self._value - other._value)
                return self
            else:
                raise ValueError('operands should have same modulus')
        raise TypeError(f'unsupported operand type(s) for +: \'Mod\' and {type(other).__name__!r}')

    def __imul__(self, other):
        if isinstance(other, int):
            self._set_value(self._value * other)
            return self
        if isinstance(other, Mod):
            if self._modulus == other._modulus:
                self._set_value(self._value * other._value)
                return self
            else:
                raise ValueError('operands should have same modulus')
        raise TypeError(f'unsupported operand type(s) for +: \'Mod\' and {type(other).__name__!r}')

    def __ipow__(self, other):
        if isinstance(other, int):
            self._set_value(self._value ** other)
            return self
        if isinstance(other, Mod):
            if self._modulus == other._modulus:
                self._set_value(self._value ** other._value)
                return self
            else:
                raise ValueError('operands should have same modulus')
        raise TypeError(f'unsupported operand type(s) for +: \'Mod\' and {type(other).__name__!r}')
    
