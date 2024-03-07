class IntegerField:
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('{self.name} value must be an int')
        if self.min_value is not None and value < self.min_value:
            raise ValueError('{self.name} value cannot be less than {self.min_value}')
        if self.max_value is not None and value > self.max_value:
            raise ValueError('{self.name} value cannot be greater than {self.max_value}')
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
class CharField:
    def __init__(self, min_length=None, max_length=None):
        # self.min_length = max(0, min_length or 0)
        self.min_length = min_length
        self.max_length = max_length

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError('{self.name} value must be a str')
        value = value.strip()
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError('{self.name} length cannot be less than {self.min_length}')
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError('{self.name} length cannot be greater than {self.max_length}')
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)