import unittest

# from app.models.field_validators import IntegerField, CharField
from app.models.field_validators_v2 import IntegerField, CharField

class TestIntegerField(unittest.TestCase):
    @staticmethod
    def create_test_class(min_=None, max_=None):
        obj = type('TestClass', (), {'age': IntegerField(min_, max_)})
        return obj()
        
    def test_set_age_ok(self):
        """Tests that valid values can be assigned/retrieved"""
        min_ = 5
        max_ = 10
        obj = self.create_test_class(min_, max_)
        valid_values = range(min_, max_)
        
        for i, value in enumerate(valid_values):
            with self.subTest(test_number=i):
                obj.age = value
                self.assertEqual(value, obj.age)
                
    def test_set_age_invalid(self):
        """Tests that invalid values raise ValueErrors or TypeError"""
        min_ = -10
        max_ = 10
        obj = self.create_test_class(min_, max_)
        bad_values = list(range(min_ - 5, min_)) + list(range(max_ + 1, max_ + 6))
        
        for i, value in enumerate(bad_values):
            with self.subTest(test_number=i):
                with self.assertRaises(ValueError):
                    obj.age = value

        bad_values = [10.5, 1 + 0j, 'abc', (1, 2)]      
        for i, value in enumerate(bad_values):
            with self.subTest(test_number=i):
                with self.assertRaises(TypeError):
                    obj.age = value

    def test_class_get(self):
        """Tests that class attribute retrieval returns the descriptor instance"""
        obj = self.create_test_class()
        obj_class = type(obj)
        self.assertIsInstance(obj_class.age, IntegerField)
        
    def test_set_age_min_only(self):
        """Tests that we can specify a min value only"""
        min_ = 0
        obj = self.create_test_class(min_)
        values = range(min_, min_ + 100, 10)
        for i, value in enumerate(values):
            with self.subTest(test_number=i):
                obj.age = value
                self.assertEqual(value, obj.age)
                
    def test_set_age_max_only(self):
        """Tests that we can specify a max value only"""
        max_ = 10
        obj = self.create_test_class(max_=max_)
        values = range(max_ - 100, max_, 10)
        for i, value in enumerate(values):
            with self.subTest(test_number=i):
                obj.age = value
                self.assertEqual(value, obj.age)
                
    def test_set_age_no_limits(self):
        """Tests that we can use IntegerField without any limits at all"""
        obj = self.create_test_class()
        values = range(-100, 100, 10)
        for i, value in enumerate(values):
            with self.subTest(test_number=i):
                obj.age = value
                self.assertEqual(value, obj.age)

class TestCharField(unittest.TestCase):
    @staticmethod
    def create_test_class(min_=None, max_=None):
        obj = type('TestClass', (), {'name': CharField(min_, max_)})
        return obj()
        
    def test_set_name_ok(self):
        """Tests that valid values can be assigned/retrieved"""
        min_ = 1
        max_ = 10
        obj = self.create_test_class(min_, max_)
        valid_lengths = range(min_, max_)
        
        for i, length in enumerate(valid_lengths):
            value = 'a' * length
            with self.subTest(test_number=i):
                obj.name = value
                self.assertEqual(value, obj.name)
            
    def test_set_name_invalid(self):
        """Tests that invalid values raise ValueErrors or TypeError"""
        min_ = 5
        max_ = 10
        obj = self.create_test_class(min_, max_)
        bad_lengths = list(range(min_ - 5, min_)) + list(range(max_ + 1, max_ + 6))
        for i, length in enumerate(bad_lengths):
            value = 'a' * length
            with self.subTest(test_number=i):
                with self.assertRaises(ValueError):
                    obj.name = value
        
        bad_values = [1, 1.1, ['a'], 5j]
        for i, value in enumerate(bad_values):
            with self.subTest(test_number=i):
                with self.assertRaises(TypeError):
                    obj.name = value
                    
    def test_class_get(self):
        """Tests that class attribute retrieval returns the descriptor instance"""
        obj = self.create_test_class(0, 0)
        obj_class = type(obj)
        self.assertIsInstance(obj_class.name, CharField)
        
    def test_set_name_min_only(self):
        """Tests that we can specify a min length only"""
        min_ = 0
        obj = self.create_test_class(min_)
        valid_lengths = range(min_, min_ + 100, 10)
        for i, length in enumerate(valid_lengths):
            value = 'a' * length
            with self.subTest(test_number=i):
                obj.name = value
                self.assertEqual(value, obj.name)
    
    # def test_set_name_min_negative_or_none(self):
    #     """Tests that setting a negative or None length results in a zero length"""
    #     obj = self.create_test_class(-10, 100)
    #     self.assertEqual(type(obj).name._min, 0)
    #     self.assertEqual(type(obj).name._max, 100)
        
    #     obj = self.create_test_class()
    #     self.assertEqual(type(obj).name._min, 0)
    #     self.assertIsNone(type(obj).name._max)
        
    def test_set_name_max_only(self):
        """Tests that we can specify a max length only"""
        max_ = 10
        obj = self.create_test_class(max_=max_)
        valid_lengths = range(max_ - 100, max_, 10)
        for i, length in enumerate(valid_lengths):
            value = 'a' * length # 'a' * -1 returns ''
            with self.subTest(test_number=i):
                obj.name = value
                self.assertEqual(value, obj.name)
                
    def test_set_name_no_limits(self):
        """Tests that we can use CharField without any limits at all"""
        obj = self.create_test_class()
        valid_lengths = range(0, 100, 10)
        for i, length in enumerate(valid_lengths):
            value = 'a' * length
            with self.subTest(test_number=i):
                obj.name = value
                self.assertEqual(value, obj.name)
                
    def test_set_name_strip(self):
        """Tests that values will be stripped when get stored"""
        obj = self.create_test_class()
        values = [' abc', 'ab ', ' add ddd ']
        for i, value in enumerate(values):
            with self.subTest(test_number=i):
                obj.name = value
                self.assertEqual(obj.name, value.strip())

def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

run_tests(TestIntegerField)
run_tests(TestCharField)