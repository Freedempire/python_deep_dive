import unittest
# from mod import Mod
from mod_v2 import Mod

def run_tests(test_case_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_case_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

class ModTestCase(unittest.TestCase):
    def test_create_mod_instance(self):
        # exception cases
        self.assertRaises(TypeError, Mod, 1.1, 10)
        self.assertRaises(TypeError, Mod, 2, 1.1)
        self.assertRaises(TypeError, Mod, 2, 'a')
        self.assertRaises(ValueError, Mod, 2, 0)
        self.assertRaises(ValueError, Mod, 2, -2)

        # success cases
        self.assertEqual(Mod(15, 12).value, 3)
        self.assertEqual(Mod(15, 12).modulus, 12)

        # exception cases
        self.assertRaises(AttributeError, setattr, Mod(1, 1), 'value', 2)
        self.assertRaises(AttributeError, setattr, Mod(1, 1), 'modulus', 2)

    def test_eq(self):
        self.assertEqual(Mod(10, 12), Mod(22, 12))
        self.assertEqual(Mod(10, 12), 10)
        self.assertEqual(Mod(10, 12), 22)
        self.assertNotEqual(Mod(10, 12), 12)
        self.assertNotEqual(Mod(10, 12), Mod(9, 12))
        self.assertRaises(TypeError, lambda: Mod(10, 12) == 'a')
        self.assertRaises(ValueError, lambda: Mod(10, 12) == Mod(10, 11))

    def test_hash(self):
        self.assertEqual(hash(Mod(1, 2)), hash(Mod(3, 2)))
        self.assertNotEqual(hash(Mod(1, 2)), hash(Mod(2, 2)))

    def test_int(self):
        self.assertEqual(int(Mod(12, 12)), 0)
        self.assertEqual(int(Mod(13, 12)), 1)

    def test_neg(self):
        self.assertEqual(-Mod(1, 12), Mod(-1, 12))

    def test_add(self):
        self.assertEqual(Mod(10, 12) + 2, Mod(0, 12))
        self.assertEqual(Mod(10, 12) + Mod(2, 12), Mod(0, 12))
        self.assertRaises(ValueError, lambda: Mod(10, 12) + Mod(10, 2))
        self.assertRaises(TypeError, lambda: Mod(10, 12) + 3.1)
        self.assertRaises(TypeError, lambda: Mod(10, 12) + 'a')

    def test_iadd(self):
        mod1 = Mod(10, 12)
        mod2 = Mod(2, 12)
        id_mod = id(mod1)
        mod1 += 2
        self.assertEqual(mod1, Mod(0, 12))
        self.assertEqual(id_mod, id(mod1))
        mod1 += mod2
        self.assertEqual(mod1, Mod(2, 12))
        self.assertRaises(ValueError, lambda: Mod(10, 12).__iadd__(Mod(10, 2)))
        self.assertRaises(TypeError, lambda: Mod(10, 12).__iadd__(3.1))
        self.assertRaises(TypeError, lambda: Mod(10, 12).__iadd__('a'))

    def test_sub(self):
        self.assertEqual(Mod(10, 12) - 2, Mod(8, 12))
        self.assertEqual(Mod(10, 12) - Mod(2, 12), Mod(8, 12))
        self.assertRaises(ValueError, lambda: Mod(10, 12) - Mod(10, 2))
        self.assertRaises(TypeError, lambda: Mod(10, 12) - 3.1)
        self.assertRaises(TypeError, lambda: Mod(10, 12) - 'a')

    def test_isub(self):
        mod1 = Mod(10, 12)
        mod2 = Mod(2, 12)
        id_mod = id(mod1)
        mod1 -= 2
        self.assertEqual(mod1, Mod(8, 12))
        self.assertEqual(id_mod, id(mod1))
        mod1 -= mod2
        self.assertEqual(mod1, Mod(6, 12))
        self.assertRaises(ValueError, lambda: Mod(10, 12).__isub__(Mod(10, 2)))
        self.assertRaises(TypeError, lambda: Mod(10, 12).__isub__(3.1))
        self.assertRaises(TypeError, lambda: Mod(10, 12).__isub__('a'))

    def test_mul(self):
        self.assertEqual(Mod(10, 12) * 2, Mod(20, 12))
        self.assertEqual(Mod(10, 12) * Mod(2, 12), Mod(20, 12))
        self.assertRaises(ValueError, lambda: Mod(10, 12) * Mod(10, 2))
        self.assertRaises(TypeError, lambda: Mod(10, 12) * 3.1)
        self.assertRaises(TypeError, lambda: Mod(10, 12) * 'a')

    def test_imul(self):
        mod1 = Mod(10, 12)
        mod2 = Mod(2, 12)
        id_mod = id(mod1)
        mod1 *= 2
        self.assertEqual(mod1, Mod(8, 12))
        self.assertEqual(id_mod, id(mod1))
        mod1 *= mod2
        self.assertEqual(mod1, Mod(4, 12))
        self.assertRaises(ValueError, lambda: Mod(10, 12).__imul__(Mod(10, 2)))
        self.assertRaises(TypeError, lambda: Mod(10, 12).__imul__(3.1))
        self.assertRaises(TypeError, lambda: Mod(10, 12).__imul__('a'))

    def test_pow(self):
        self.assertEqual(Mod(10, 12) ** 2, Mod(100, 12))
        self.assertEqual(Mod(10, 12) ** Mod(2, 12), Mod(100, 12))
        self.assertRaises(ValueError, lambda: Mod(10, 12) ** Mod(10, 2))
        self.assertRaises(TypeError, lambda: Mod(10, 12) ** 3.1)
        self.assertRaises(TypeError, lambda: Mod(10, 12) ** 'a')

    def test_ipow(self):
        mod1 = Mod(10, 12)
        mod2 = Mod(2, 12)
        id_mod = id(mod1)
        mod1 **= 2
        self.assertEqual(mod1, Mod(4, 12))
        self.assertEqual(id_mod, id(mod1))
        mod1 **= mod2
        self.assertEqual(mod1, Mod(4, 12))
        self.assertRaises(ValueError, lambda: Mod(10, 12).__ipow__(Mod(10, 2)))
        self.assertRaises(TypeError, lambda: Mod(10, 12).__ipow__(3.1))
        self.assertRaises(TypeError, lambda: Mod(10, 12).__ipow__('a'))

    def test_ordering(self):
        mod1 = Mod(3, 12)
        mod2 = Mod(5, 12)
        mod3 = Mod(30, 12)
        mod4 = Mod(15, 12)
        self.assertRaises(TypeError, lambda: mod1 > 1.1)
        self.assertRaises(TypeError, lambda: mod1 < 1.1)
        self.assertRaises(TypeError, lambda: mod1 <= 1.1)
        self.assertRaises(TypeError, lambda: mod1 != 1.1)
        self.assertRaises(TypeError, lambda: mod1 >= 1.1)
        self.assertRaises(ValueError, lambda: mod1 >= Mod(3, 11))
        self.assertTrue(mod1 < mod2)
        self.assertTrue(mod1 <= mod2)
        self.assertTrue(mod2 > mod1)
        self.assertTrue(mod2 >= mod1)
        self.assertTrue(mod3 > mod2)
        self.assertTrue(mod3 != mod2)
        self.assertTrue(mod1 == mod4)


run_tests(ModTestCase)