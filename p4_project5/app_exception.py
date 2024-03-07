from enum import Enum, auto

class AppException(Enum):
    def __new__(cls, member_code, member_exc_type, member_default_msg):
        member = object.__new__(cls)
        member._value_ = member_code
        member.exc_type = member_exc_type
        member.default_msg = member_default_msg
        return member
    
    NotAnInteger = auto(), TypeError, 'value is not an integer'
    Timeout = auto(), RuntimeError, 'timeout error'

    @property
    def code(self):
        return self.value
    
    def throw(self, msg=None):
        msg = msg or self.default_msg
        raise self.exc_type(f'{self.name}: {msg}')
    
print(list(AppException))
print(AppException.Timeout)
print(AppException(2))
print(AppException['Timeout'])
print(AppException.Timeout.code)
print(AppException.Timeout.value)
print(AppException.Timeout.name)
print(AppException.Timeout.exc_type)
print(AppException.Timeout.default_msg)
try:
    # AppException.NotAnInteger.throw('custom message')
    AppException.NotAnInteger.throw()
except AppException.NotAnInteger.exc_type as e:
    print(e)