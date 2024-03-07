from functools import total_ordering
import operator

@total_ordering
class Mod:
    def __init__(self, value, modulus):
        if not isinstance(modulus, int):
            raise TypeError('modulus should be of int type')
        if modulus <= 0:
            raise ValueError('modulus should be positive')
        if not isinstance(value, int):
            raise TypeError('value should be of int type')
        
        self._modulus = modulus
        self._value = value % modulus

    @property
    def value(self):
        return self._value
    
    @property
    def modulus(self):
        return self._modulus
    
    def _get_value(self, other):
        if isinstance(other, int):
            return other % self._modulus
        if isinstance(other, Mod):
            if self._modulus == other._modulus:
                return other._value
            else:
                raise ValueError('operation unsupported between Mod instances with different moduli')
        raise TypeError(f'unsupported operand type(s) for +: \'Mod\' and {type(other).__name__!r}')
    
    def _arithmetic_operation(self, other, operation, *, in_place=False):
        other_value = self._get_value(other)
        result = operation(self._value, other_value)
        if in_place:
            self._value = result % self._modulus
            return self
        return Mod(result, self._modulus)

    def __repr__(self):
        return f'Mod(value={self._value}, modulus={self._modulus})'
    
    def __lt__(self, other):
        return self._value < self._get_value(other)

    def __eq__(self, other):
        return self._value == self._get_value(other)
    
    def __hash__(self):
        return hash((self._value, self._modulus))
    
    def __int__(self):
        return self._value
    
    def __neg__(self):
        return Mod(-self._value, self._modulus)
    
    def __add__(self, other):
        return self._arithmetic_operation(other, operator.add)

    def __sub__(self, other):
        return self._arithmetic_operation(other, operator.sub)

    def __mul__(self, other):
        return self._arithmetic_operation(other, operator.mul)

    def __pow__(self, other):
        return self._arithmetic_operation(other, operator.pow)

    def __iadd__(self, other):
        return self._arithmetic_operation(other, operator.add, in_place=True)

    def __isub__(self, other):
        return self._arithmetic_operation(other, operator.sub, in_place=True)


    def __imul__(self, other):
        return self._arithmetic_operation(other, operator.mul, in_place=True)


    def __ipow__(self, other):
        return self._arithmetic_operation(other, operator.pow, in_place=True)