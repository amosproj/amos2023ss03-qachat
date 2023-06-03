import unittest
from QAChat.db_interface import DBInterface



class DatabaseIntegrationTest(unittest.TestCase):

    def test_init(self):
        try:
            db = DBInterface()
            print("hello world")
        except ConnectionError as e:
            print("Connection Error:", e)
      

if __name__ == '__main__':
    unittest.main()
