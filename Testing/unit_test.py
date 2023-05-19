import unittest
from add_file import add

class TestAdd(unittest.TestCase):
    def test_add(self):
        result = add(1,1)
        self.assertEqual(result, 2)

if __name__ == "__main__":
    unittest.main()
