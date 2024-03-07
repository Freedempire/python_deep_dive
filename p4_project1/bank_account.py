from datetime import datetime, timezone, timedelta
from decimal import Decimal
import os
import re
from collections import namedtuple

Transaction = namedtuple('Transaction', 'transaction_type account_id transaction_datetime transaction_datetime_preferred random_code')

class BankAccount:
    _TRANSACTION_TYPES = {'deposit': 'D', 'withdraw': 'W', 'pay_interest': 'I', 'declined': 'X'}
    _monthly_interest_rate = Decimal('0.005')
    _account_ids = set()

    @classmethod
    def get_monthly_interest_rate(cls):
        return str(cls._monthly_interest_rate)
    
    @classmethod
    def set_monthly_interest_rate(cls, monthly_interest_rate):
        if cls.validate_interest_rate(monthly_interest_rate): # exclude strings like 'inf', '-Infinity', 'nan', 'snan', 'snan1' that are acceptable to Decimal()
            cls._monthly_interest_rate = Decimal(monthly_interest_rate)
        else:
            raise ValueError('Internal error: the interest rate should be a numeric string')

    @classmethod
    def generate_account_id(cls, length=18):
        # generate a string of digits with designated length (default to 18), and check the 
        while True:
            account_id = cls.generate_random_digits(length)

            if account_id not in cls._account_ids:
                cls._account_ids.add(account_id)
                break
        return account_id
    
    @classmethod
    def parse_transaction_code(cls, transaction_code, preferred_timezone=None):
        transaction_parameters = transaction_code.split('-')
        # find corresponding transaction_type according to type_code
        for k, v in cls._TRANSACTION_TYPES.items():
            if v == transaction_parameters[0]:
                transaction_type = k
                break
        account_id = transaction_parameters[1]
        transaction_datetime = datetime.strptime(transaction_parameters[2], '%Y%m%d%H%M%S%f').replace(tzinfo=timezone.utc)
        if preferred_timezone is None:
            transaction_datetime_preferred = transaction_datetime
        else:
            transaction_datetime_preferred = transaction_datetime.astimezone(preferred_timezone)
        random_code = transaction_parameters[3]
        return Transaction(transaction_type, account_id, transaction_datetime, transaction_datetime_preferred, random_code)

    @staticmethod
    def generate_random_digits(length):
        # random bytes -> int -> str of digits -> slice the last n digits -> fill with 0 from left if not enough digits
        return f'{str(int.from_bytes(os.urandom(8)))[-length:]:0>{length}}'
    
    # @staticmethod
    # def validate_name(name):
    #     pattern = r'^[a-zA-Z]+$'
    #     return bool(re.match(pattern, name))

    @staticmethod
    def formalize_name(name, field):
        name = name.strip().capitalize()
        if name.isalpha():
            return name
        else:
            raise ValueError(f'{field} should be non-empty and can only contains alphabets')
    
    @staticmethod
    def validate_interest_rate(interest_rate):
        # match a string of integer or float with arbitrary decimal places, allowing prefixing or trailing whitespaces
        pattern = r'^\s*[+-]?\d+(\.\d+)?\s*$'
        return bool(re.match(pattern, interest_rate))

    @staticmethod
    def validate_amount(amount):
        # match a string of positive integer or float with 2 decimal places at most, allowing prefixing or trailing whitespaces
        pattern = r'^\s*\d+(\.\d{1,2})?\s*$'
        return re.match(pattern, amount) and float(amount) > 0
    
    @staticmethod
    def get_timezone(hours_offset):
        if hours_offset is None:
            return timezone.utc
        return timezone(timedelta(hours=hours_offset))

    def __init__(self, firstname, lastname, hours_offset=None):
        self._account_id = self.generate_account_id()
        self.firstname = firstname
        self.lastname = lastname
        self.preferred_timezone = hours_offset
        self._balance = Decimal(0)

    @property
    def account_id(self):
        return self._account_id
    
    @property
    def firstname(self):
        return self._firstname
    
    @firstname.setter
    def firstname(self, firstname):
        # firstname = firstname.strip().capitalize()
        # # if self.validate_name(firstname):
        # if firstname.isalpha():
        #     self._firstname = firstname
        #     self._fullname = None
        # else:
        #     raise ValueError('name should be non-empty and can only contain alphabets')
        self._firstname = self.formalize_name(firstname, 'first name')
        self._fullname = None
        
    @property
    def lastname(self):
        return self._lastname
    
    @lastname.setter
    def lastname(self, lastname):
        # lastname = lastname.strip().capitalize()
        # if lastname.isalpha():
        #     self._lastname = lastname
        #     self._fullname = None
        # else:
        #     raise ValueError('name should be non-empty and can only contain alphabets')
        self._lastname = self.formalize_name(lastname, 'last name')
        self._fullname = None
        
    @property
    def fullname(self):
        if self._fullname is None:
            self._fullname = f'{self._firstname} {self._lastname}'
        return self._fullname
    
    @property
    def preferred_timezone(self):
        return self._preferred_timezone
    
    @preferred_timezone.setter
    def preferred_timezone(self, hours_offset):
        self._preferred_timezone = self.get_timezone(hours_offset)

    @property
    def preferred_timezone_name(self):
        return str(self._preferred_timezone)
    
    @property
    def balance(self):
        return f'{self._balance:.2f}' # stringified and rounded
    
    # use class method instead
    # @property
    # def monthly_interest_rate(self):
    #     return str(self._monthly_interest_rate)
    
    def deposit(self, amount):
        if self.validate_amount(amount):
            self._balance += Decimal(amount)
            return self.generate_transaction_code('deposit')
        else:
            raise ValueError('Internal error: the amount should be a string of positive integer or float with 2 decimal places at most')

    def withdraw(self, amount):
        if self.validate_amount(amount):
            amount = Decimal(amount)
            if self._balance >= amount:
                self._balance -= amount
                return self.generate_transaction_code('withdraw')
            else:
                return self.generate_transaction_code('declined')
        else:
            raise ValueError('Internal error: the amount should be a string of positive integer or float with 2 decimal places at most')

    def pay_interest(self):
        self._balance *= (Decimal(1) + self._monthly_interest_rate)
        return self.generate_transaction_code('pay_interest')

    def generate_transaction_code(self, transaction_type): # generate code like transaction_type - account_id - datetime - random_digits
        if transaction_type not in self._TRANSACTION_TYPES:
            raise ValueError('Internal error: invalid transaction type')
        type_code = self._TRANSACTION_TYPES[transaction_type]
        datetime_code = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')
        random_code = self.generate_random_digits(6)
        return f'{type_code}-{self._account_id}-{datetime_code}-{random_code}'
    

# manual tests

# print(BankAccount.validate_amount(''))
# print(BankAccount.validate_amount('.'))
# print(BankAccount.validate_amount('-1'))
# print(BankAccount.validate_amount(' 1 '))
# print(BankAccount.validate_amount(' 12 '))
# print(BankAccount.validate_amount('123'))
# print(BankAccount.validate_amount('123.'))
# print(BankAccount.validate_amount('1.1'))
# print(BankAccount.validate_amount('11.11'))
# print(BankAccount.validate_amount('11.111'))
# print(BankAccount.validate_amount('333431.11'))
# print(BankAccount.generate_account_id())

# ba = BankAccount('tony', 'king', 11)
# print(f'{ba.firstname = }')
# print(f'{ba.lastname = }')
# print(f'{ba.fullname = }')
# ba.firstname = 'tom'
# print(f'{ba.fullname = }')
# print(f'{ba.preferred_timezone_name = }')
# print(f'{ba.preferred_timezone = }')
# ba.preferred_timezone = 5
# print(f'{ba.preferred_timezone_name = }')
# print(f'{ba.account_id = }')
# print(f'{ba.balance = }')
# print(f'{ba.get_monthly_interest_rate() = }')
# ba.set_monthly_interest_rate('0.1')
# print(f'{ba.get_monthly_interest_rate() = }')
# d_transaction = ba.deposit('10000.12')
# # d_transaction = ba.deposit('-10000.12')
# print(f'{ba.balance = }')
# transaction1 = ba.parse_transaction_code(d_transaction)
# transaction2 = ba.parse_transaction_code(d_transaction, ba.preferred_timezone)
# transaction3 = ba.parse_transaction_code(d_transaction, timezone(timedelta(hours=8)))
# print(f'{d_transaction = }')
# print(f'{transaction1 = }')
# print(f'{transaction2 = }')
# print(f'{transaction3 = }')
# w_transaction = ba.withdraw('500.12')
# print(f'{w_transaction = }')
# print(f'{ba.balance = }')
# w_transaction = ba.withdraw('10000')
# print(f'{w_transaction = }')
# i_transaction = ba.pay_interest()
# print(f'{i_transaction = }')
# print(f'{ba.balance = }')