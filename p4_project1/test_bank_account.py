import unittest
from bank_account import BankAccount, Transaction
from datetime import datetime, timezone, timedelta
from decimal import Decimal

def run_tests(test_case_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_case_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


class BankAccountTestCase(unittest.TestCase):
    # to define instructions (test fixture) that will be executed immediately before each test method
    # def setUp(self):
    #     pass

    # to define instructions (test fixture) that will be executed immediately after each test method even if the test method raise an exception
    # def tearDown(self):
    #     pass

    def test_get_monthly_interest_rate(self):
        self.assertEqual(BankAccount.get_monthly_interest_rate(), '0.005')

    def test_set_monthly_interest_rate(self):
        # exception cases
        self.assertRaises(ValueError, BankAccount.set_monthly_interest_rate, '')
        self.assertRaises(ValueError, BankAccount.set_monthly_interest_rate, '.1')
        self.assertRaises(ValueError, BankAccount.set_monthly_interest_rate, 'a')
        self.assertRaises(ValueError, BankAccount.set_monthly_interest_rate, 'inf')
        self.assertRaises(ValueError, BankAccount.set_monthly_interest_rate, '-inf')
        self.assertRaises(ValueError, BankAccount.set_monthly_interest_rate, 'infinity')
        self.assertRaises(ValueError, BankAccount.set_monthly_interest_rate, 'nan')
        self.assertRaises(ValueError, BankAccount.set_monthly_interest_rate, '1a')
        self.assertRaises(ValueError, BankAccount.set_monthly_interest_rate, '1..2')
        self.assertRaises(TypeError, BankAccount.set_monthly_interest_rate, 0.001)

        # success cases
        BankAccount.set_monthly_interest_rate('0.001')
        self.assertEqual(BankAccount.get_monthly_interest_rate(), '0.001')
        BankAccount.set_monthly_interest_rate('-0.001')
        self.assertEqual(BankAccount.get_monthly_interest_rate(), '-0.001')

    def test_generate_account_id(self):
        account_id = BankAccount.generate_account_id()
        self.assertEqual(len(account_id), 18)
        self.assertTrue(account_id.isdigit())
        self.assertTrue(account_id in BankAccount._account_ids)

        account_id = BankAccount.generate_account_id(length=16)
        self.assertEqual(len(account_id), 16)

    def test_get_timezone(self):
        self.assertEqual(BankAccount.get_timezone(None), timezone.utc)
        self.assertEqual(BankAccount.get_timezone(10), timezone(timedelta(hours=10)))

    def test_instance_properties(self):
        firstname = 'john'
        lastname = 'cleese'
        hours_offset = 10
        ba1 = BankAccount(firstname, lastname, hours_offset)

        self.assertTrue(ba1.account_id in BankAccount._account_ids)
        self.assertEqual(ba1.firstname, firstname.capitalize())
        self.assertEqual(ba1.lastname, lastname.capitalize())
        self.assertEqual(ba1.fullname, f'{firstname.capitalize()} {lastname.capitalize()}')
        self.assertEqual(ba1.preferred_timezone, timezone(timedelta(hours=hours_offset)))
        self.assertEqual(ba1.balance, '0.00')

        firstname = ' john '
        lastname = ' cleese '
        ba2 = BankAccount(firstname, lastname)

        self.assertTrue(ba2.account_id in BankAccount._account_ids)
        self.assertNotEqual(ba2.account_id, ba1.account_id)
        self.assertEqual(ba2.firstname, firstname.strip().capitalize())
        self.assertEqual(ba2.lastname, lastname.strip().capitalize())
        self.assertEqual(ba2.preferred_timezone, timezone.utc)
        self.assertEqual(ba2.preferred_timezone_name, str(timezone.utc))
        self.assertEqual(ba2.balance, '0.00')

        # exception cases
        self.assertRaises(ValueError, setattr, ba1, 'firstname', '')
        self.assertRaises(ValueError, setattr, ba1, 'firstname', ' ')
        self.assertRaises(ValueError, setattr, ba1, 'firstname', '123')
        self.assertRaises(ValueError, setattr, ba1, 'firstname', '123aa')
        self.assertRaises(ValueError, setattr, ba1, 'firstname', 'john cleese')
        self.assertRaises(ValueError, setattr, ba1, 'lastname', '')
        self.assertRaises(ValueError, setattr, ba1, 'lastname', ' ')
        self.assertRaises(ValueError, setattr, ba1, 'lastname', '123')
        self.assertRaises(ValueError, setattr, ba1, 'lastname', '123aa')
        self.assertRaises(ValueError, setattr, ba1, 'lastname', 'john cleese')

    def test_instance_methods(self):
        ba = BankAccount('john', 'cleese')
        balance = Decimal(ba.balance)

        # deposit
        ba.deposit('100.3')
        self.assertEqual(ba.balance, f'{balance + Decimal('100.3'):.2f}')
        # exception cases
        self.assertRaises(ValueError, ba.deposit, '')
        self.assertRaises(ValueError, ba.deposit, ' ')
        self.assertRaises(ValueError, ba.deposit, '0')
        self.assertRaises(ValueError, ba.deposit, '0.0')
        self.assertRaises(ValueError, ba.deposit, 'inf')
        self.assertRaises(ValueError, ba.deposit, 'nan')
        self.assertRaises(ValueError, ba.deposit, '-1')
        self.assertRaises(TypeError, ba.deposit, 100)

        # withdraw
        ba.withdraw('10.29')
        self.assertEqual(ba.balance, f'{balance + Decimal('100.3') - Decimal('10.29'):.2f}')

        transaction_code = ba.withdraw('1000')
        self.assertEqual(transaction_code[0], 'X')
        
        # exception cases
        self.assertRaises(ValueError, ba.withdraw, '')
        self.assertRaises(ValueError, ba.withdraw, ' ')
        self.assertRaises(ValueError, ba.withdraw, '0')
        self.assertRaises(ValueError, ba.withdraw, '0.0')
        self.assertRaises(ValueError, ba.withdraw, 'inf')
        self.assertRaises(ValueError, ba.withdraw, 'nan')
        self.assertRaises(ValueError, ba.withdraw, '-1')
        self.assertRaises(TypeError, ba.withdraw, 100)

    def test_generate_transaction_code(self):
        ba = BankAccount('john', 'cleese')

        self.assertRaises(ValueError, ba.generate_transaction_code, 'other')

    def test_parse_transaction_code(self):
        ba = BankAccount('ben', 'son')
        transaction_code = ba.deposit('100')
        transaction = BankAccount.parse_transaction_code(transaction_code, timezone.utc)

        self.assertTrue(isinstance(transaction, Transaction))
        self.assertTrue(transaction.transaction_type in BankAccount._TRANSACTION_TYPES)
        self.assertEqual(transaction.account_id, ba.account_id)
        self.assertEqual(transaction.transaction_datetime, transaction.transaction_datetime_preferred)
        self.assertEqual(len(transaction.random_code), 6)
        self.assertTrue(transaction.random_code.isdigit())

run_tests(BankAccountTestCase)