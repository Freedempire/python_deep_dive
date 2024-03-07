class BaseValidator:
    def __init__(self, min_=None, max_=None):
        self.min = min_
        self.max = max_

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        value = self.validate(value)
        instance.__dict__[self.name] = value

    def validate(self, value):
        """need to be implemented by each subclass"""
        return value

class IntegerField(BaseValidator):
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError('{self.name} value must be an int')
        if self.min is not None and value < self.min:
            raise ValueError('{self.name} value cannot be less than {self.min}')
        if self.max is not None and value > self.max:
            raise ValueError('{self.name} value cannot be greater than {self.max}')
        return value

class CharField(BaseValidator):
    # def __init__(self, min_=None, max_=None):
    #     min_ = max(0, min_ or 0)
    #     super().__init__(min_, max_)

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError('{self.name} value must be a str')
        value = value.strip()
        if self.min is not None and len(value) < self.min:
            raise ValueError('{self.name} length cannot be less than {self.min}')
        if self.max is not None and len(value) > self.max:
            raise ValueError('{self.name} length cannot be greater than {self.max}')
        return value
