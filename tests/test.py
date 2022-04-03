import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest import TestCase

from main import parser

directory = "tests\\resources"

class TestParser(TestCase):
    def test_parser(self):
        for filename in os.listdir(directory):
            file = os.path.join(directory, filename)
            try:
                f = open(file)
                parser.parse(f.read())
            except Exception as e:
                self.fail("Could not parse " + file + ":\n" + str(e))
            f.close()

if __name__ == '__main__':
    unittest.main()
