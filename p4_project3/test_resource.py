import unittest
from resource import Resource, CPU, Storage, HDD, SSD

def run_tests(test_case_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_case_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

class ResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.name = 'resource'
        self.manufacturer = 'maker'
        self.inventory = 100
        self.allocated = 0
        self.r = Resource(self.name, self.manufacturer, self.inventory, self.allocated)

    def test_instance_creation(self):
        self.assertRaises(TypeError, Resource, 1, 1, 1, 1)
        self.assertRaises(TypeError, Resource, 'resource', 1, 1, 1)
        self.assertRaises(TypeError, Resource, 'resource', 'maker', '1', 1)
        self.assertRaises(TypeError, Resource, 'resource', 'maker', 10, '1')
        self.assertRaises(TypeError, Resource, 'resource', 'maker', 10, 1.0)
        self.assertRaises(ValueError, Resource, 'resource', 'maker', -10, 1)
        self.assertRaises(ValueError, Resource, 'resource', 'maker', 10, -1)

    def test_instance_attributes(self):
        self.assertEqual(self.r.name, self.name)
        self.assertEqual(self.r.manufacturer, self.manufacturer)
        self.assertEqual(self.r.inventory, self.inventory)
        self.assertEqual(self.r.allocated, self.allocated)
        self.assertRaises(AttributeError, setattr, self.r, 'new_attribute', 1)
        self.assertRaises(AttributeError, setattr, self.r, 'name', 'new_name')
        self.assertRaises(AttributeError, setattr, self.r, 'manufacturer', 'new_maker')
        self.assertRaises(AttributeError, setattr, self.r, 'inventory', 20)
        self.assertRaises(AttributeError, setattr, self.r, 'allocated', 10)

    def test_claim(self):
        self.assertRaises(ValueError, self.r.claim, -1)
        self.assertRaises(ValueError, self.r.claim, 0)
        self.assertRaises(ValueError, self.r.claim, self.r.inventory + 1)
        self.r.claim(self.r.inventory)
        self.assertEqual(self.r.inventory, 0)
        self.assertEqual(self.r.allocated, self.allocated + self.inventory)

    def test_free_up(self):
        self.assertRaises(RuntimeError, self.r.free_up, 1) # allocated 0
        self.r.claim(5)
        self.assertRaises(ValueError, self.r.free_up, -1)
        self.assertRaises(ValueError, self.r.free_up, 0)
        self.assertRaises(ValueError, self.r.free_up, self.r.allocated + 1)
        self.r.free_up(self.r.allocated)
        self.assertEqual(self.r.allocated, 0)
        self.assertEqual(self.r.inventory, self.inventory)

    def test_remove_died(self):
        self.assertRaises(ValueError, self.r.remove_died, -1)
        self.assertRaises(ValueError, self.r.remove_died, 0)
        self.assertRaises(ValueError, self.r.remove_died, self.r.inventory + 1)
        self.r.remove_died(self.r.inventory)
        self.assertAlmostEqual(self.r.inventory, 0)
        self.assertAlmostEqual(self.r.allocated, self.allocated)
        self.assertRaises(RuntimeError, self.r.remove_died, 1)

    def test_add_purchased(self):
        self.assertRaises(ValueError, self.r.add_purchased, 0)
        self.assertRaises(ValueError, self.r.add_purchased, -2)
        self.assertRaises(ValueError, self.r.add_purchased, 2.0)
        self.r.add_purchased(10)
        self.assertEqual(self.r.inventory, self.inventory + 10)

    def test_category(self):
        self.assertEqual(self.r.category(), 'resource')

class CPUTestCase(unittest.TestCase):
    def test_all(self):
        cpu = CPU('AMD Ryzen', 'AMD', 100, 10, 24, 'A10', 28)
        self.assertEqual(cpu.cores, 24)
        self.assertEqual(cpu.socket, 'A10')
        self.assertEqual(cpu.power_watts, 28)

class StorageTestCase(unittest.TestCase):
    def test_all(self):
        storage = Storage('WD 100T', 'WD', 20, 100, 100000)
        self.assertEqual(storage.capacity_GB, 100000)

class HDDTestCase(unittest.TestCase):
    def test_all(self):
        hdd = HDD('WD 100T', 'WD', 100, 20, 100000, '3.5"', 10000)
        self.assertEqual(hdd.size, '3.5"', 10000)

class SSDTestCase(unittest.TestCase):
    def test_all(self):
        ssd = SSD('SG 20T', 'SG', 200, 1000, 20000, 'NVMe')
        self.assertEqual(ssd.interface, 'NVMe')

run_tests(ResourceTestCase)
run_tests(CPUTestCase)
run_tests(StorageTestCase)
run_tests(HDDTestCase)
run_tests(SSDTestCase)