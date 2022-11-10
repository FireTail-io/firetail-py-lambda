import unittest


class TestSimple(unittest.TestCase):

    def test_add(self):
        self.assertEqual(((5) + (6)).value, 11)


if __name__ == '__main__':
    unittest.main()
