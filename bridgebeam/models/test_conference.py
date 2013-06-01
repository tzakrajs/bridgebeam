from conference import Conference
import unittest

class TestConferenceMethods(unittest.TestCase):
    def setUp(self):
        self.conference = Conference()
        
    def test_it_exists(self):
        self.assertTrue(isinstance(self.conference, Conference))

if __name__ == '__main__':
    unittest.main()
